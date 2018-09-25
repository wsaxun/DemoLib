import sys
import logging
import datetime
from dateutil import tz
from common.log import context as context_utils


class ContextFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        self.version = kwargs.pop('version', 'unknown')
        self.conf = kwargs.pop('config', None)
        logging.Formatter.__init__(self, *args, **kwargs)

    def format(self, record):
        record.version = self.version

        _update_record_with_context(record)

        for key in ('instance',):
            if key not in record.__dict__:
                record.__dict__[key] = ''

        if record.__dict__.get('request_id'):
            fmt = self.conf.context_format_string
        else:
            fmt = self.conf.default_format_string

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

def _dictify_context(context):
    if getattr(context, 'get_logging_values', None):
        return context.get_logging_values()
    elif getattr(context, 'to_dict', None):
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
