import sys
import logging
import six
import debtcollector
import traceback
import datetime
from dateutil import tz
from common.log import context as context_utils

_CONF = None


class ContextFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', 'unknown')
        self.version = kwargs.pop('version', 'unknown')
        self.conf = kwargs.pop('config', _CONF)
        logging.Formatter.__init__(self, *args, **kwargs)

    def format(self, record):
        if six.PY2:
            should_use_unicode = True
            args = (record.args.values() if isinstance(record.args,
                                                       dict) else record.args)
            for arg in args or []:
                try:
                    six.text_type(arg)
                except UnicodeDecodeError:
                    should_use_unicode = False
                    break
            if (not isinstance(record.msg,
                               six.text_type) and should_use_unicode):
                record.msg = _ensure_unicode(record.msg)

        record.project = self.project
        record.version = self.version

        instance_extra = ''
        instance = getattr(record, 'instance', None)
        instance_uuid = getattr(record, 'instance_uuid', None)
        context = _update_record_with_context(record)
        if instance:
            try:
                instance_extra = (self.conf.instance_format % instance)
            except TypeError:
                instance_extra = instance
        elif instance_uuid:
            instance_extra = (self.conf.instance_uuid_format % {
                'uuid': instance_uuid})
        elif context:
            instance = getattr(context, 'instance', None)
            instance_uuid = getattr(context, 'instance_uuid', None)
            resource_uuid = getattr(context, 'resource_uuid', None)

            if instance:
                instance_extra = (
                        self.conf.instance_format % {'uuid': instance})
            elif instance_uuid:
                instance_extra = (self.conf.instance_uuid_format % {
                    'uuid': instance_uuid})
            elif resource_uuid:
                instance_extra = (self.conf.instance_uuid_format % {
                    'uuid': resource_uuid})

        record.instance = instance_extra

        # NOTE(sdague): default the fancier formatting params
        # to an empty string so we don't throw an exception if
        # they get used
        for key in ('instance', 'color', 'user_identity', 'resource',
                    'user_name', 'project_name'):
            if key not in record.__dict__:
                record.__dict__[key] = ''

        # Set the "user_identity" value of "logging_context_format_string"
        # by using "logging_user_identity_format" and
        # get_logging_values of oslo.context.
        # if context:
        #     record.user_identity = (
        #         self.conf.logging_user_identity_format %
        #         _ReplaceFalseValue(_dictify_context(context))
        #     )

        if record.__dict__.get('request_id'):
            fmt = self.conf.logging_context_format_string
        else:
            fmt = self.conf.logging_default_format_string

        # Cache the formatted traceback on the record, Logger will
        # respect our formatted copy
        if record.exc_info:
            record.exc_text = self.formatException(record.exc_info, record)

        record.error_summary = _get_error_summary(record)
        if '%(error_summary)s' in fmt:
            record.error_summary = record.error_summary or '_'
        elif record.error_summary:
            # If we have not been told how to format the error and
            # there is an error to summarize, make sure the format
            # string includes the bits we need to include it.
            fmt += ': %(error_summary)s'

        if (record.levelno == logging.DEBUG and
                self.conf.logging_debug_format_suffix):
            fmt += " " + self.conf.logging_debug_format_suffix

        self._compute_iso_time(record)

        if sys.version_info < (3, 2):
            self._fmt = fmt
        else:
            self._style = logging.PercentStyle(fmt)
            self._fmt = self._style._fmt

        try:
            return logging.Formatter.format(self, record)
        except TypeError as err:
            # Something went wrong, report that instead so we at least
            # get the error message.
            record.msg = 'Error formatting log line msg={!r} err={!r}'.format(
                record.msg, err).replace('%', '*')
            return logging.Formatter.format(self, record)

    def _compute_iso_time(self, record):
        # set iso8601 timestamp
        localtz = tz.tzlocal()
        record.isotime = datetime.datetime.fromtimestamp(
            record.created).replace(tzinfo=localtz).isoformat()
        if record.created == int(record.created):
            # NOTE(stpierre): when the timestamp includes no
            # microseconds -- e.g., 1450274066.000000 -- then the
            # microseconds aren't included in the isoformat() time. As
            # a result, in literally one in a million cases
            # isoformat() looks different. This adds microseconds when
            # that happens.
            record.isotime = "%s.000000%s" % (record.isotime[:-6],
                                              record.isotime[-6:])


def _ensure_unicode(msg):
    if isinstance(msg, six.text_type):
        return msg
    if not isinstance(msg, six.binary_type):
        return six.text_type(msg)
    return safe_decode(msg, incoming='utf-8', errors='xmlcharrefreplace')


def _dictify_context(context):
    if getattr(context, 'get_logging_values', None):
        values = context.get_logging_values()
        return context.get_logging_values()
    elif getattr(context, 'to_dict', None):
        debtcollector.deprecate(
            'The RequestContext.get_logging_values() '
            'method should be defined for logging context specific '
            'information.  The to_dict() method is deprecated '
            'for oslo.log use.', version='3.8.0', removal_version='5.0.0')
        return context.to_dict()
    elif isinstance(context, dict):
        return context

    return {}


def _update_record_with_context(record):
    """Given a log record, update it with context information.

    The request context, if there is one, will either be passed with the
    incoming record or in the global thread-local store.
    """

    context = record.__dict__.get('context', context_utils.get_current())
    if context:
        d = _dictify_context(context)
        for k, v in d.items():
            setattr(record, k, v)

    return context


def safe_decode(text, incoming=None, errors='strict'):
    """Decodes incoming text/bytes string using `incoming` if they're not
       already unicode.

    :param incoming: Text's current encoding
    :param errors: Errors handling policy. See here for valid
        values http://docs.python.org/2/library/codecs.html
    :returns: text or a unicode `incoming` encoded
                representation of it.
    :raises TypeError: If text is not an instance of str
    """
    if not isinstance(text, (six.string_types, six.binary_type)):
        raise TypeError("%s can't be decoded" % type(text))

    if isinstance(text, six.text_type):
        return text

    if not incoming:
        incoming = (sys.stdin.encoding or
                    sys.getdefaultencoding())

    try:
        return text.decode(incoming, errors)
    except UnicodeDecodeError:
        # Note(flaper87) If we get here, it means that
        # sys.stdin.encoding / sys.getdefaultencoding
        # didn't return a suitable encoding to decode
        # text. This happens mostly when global LANG
        # var is not set correctly and there's no
        # default encoding. In this case, most likely
        # python will use ASCII or ANSI encoders as
        # default encodings but they won't be capable
        # of decoding non-ASCII characters.
        #
        # Also, UTF-8 is being used since it's an ASCII
        # extension.
        return text.decode('utf-8', errors)


def _get_error_summary(record):
    """Return the error summary

    If there is no active exception, return the default.

    If the record is being logged below the warning level, return an
    empty string.

    If there is an active exception, format it and return the
    resulting string.

    """
    error_summary = ''
    if record.levelno < logging.WARNING:
        return ''

    if record.exc_info:
        # Save the exception we were given so we can include the
        # summary in the log line.
        exc_info = record.exc_info
    else:
        # Check to see if there is an active exception that was
        # not given to us explicitly. If so, save it so we can
        # include the summary in the log line.
        exc_info = sys.exc_info()
        # If we get (None, None, None) because there is no
        # exception, convert it to a simple None to make the logic
        # that uses the value simpler.
        if not exc_info[0]:
            exc_info = None
        elif exc_info[0] in (TypeError, ValueError,
                             KeyError, AttributeError, ImportError):
            # NOTE(dhellmann): Do not include information about
            # common built-in exceptions used to detect cases of
            # bad or missing data. We don't use isinstance() here
            # to limit this filter to only the built-in
            # classes. This check is only performed for cases
            # where the exception info is being detected
            # automatically so if a caller gives us an exception
            # we will definitely log it.
            exc_info = None

    # If we have an exception, format it to be included in the
    # output.
    if exc_info:
        try:
            # Build the exception summary in the line with the
            # primary log message, to serve as a mnemonic for error
            # and warning cases.
            error_summary = traceback.format_exception_only(
                exc_info[0],
                exc_info[1],
            )[0].rstrip()
            # If the exc_info wasn't explicitly passed to us, take only the
            # first line of it. _Remote exceptions from oslo.messaging append
            # the full traceback to the exception message, so we want to avoid
            # outputting the traceback unless we've been passed exc_info
            # directly (via LOG.exception(), for example).
            if not record.exc_info:
                error_summary = error_summary.split('\n', 1)[0]
        except TypeError as type_err:
            # Work around https://bugs.python.org/issue28603
            error_summary = "<exception with %s>" % six.text_type(type_err)
        finally:
            # Remove the local reference to the exception and
            # traceback to avoid a memory leak through the frame
            # references.
            del exc_info

    return error_summary
