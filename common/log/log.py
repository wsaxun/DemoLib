import sys
import os
import logging
import logging.handlers
from logging import getLevelName
import inspect
import datetime
from dateutil import tz
from common.context import get_current


class BaseLoggerAdapter(logging.LoggerAdapter):
    warn = logging.LoggerAdapter.warning
    TRACE = 5

    @property
    def handlers(self):
        return self.logger.handlers

    def trace(self, msg, *args, **kwargs):
        self.log(self.TRACE, msg, *args, **kwargs)


class KeywordArgumentAdapter(BaseLoggerAdapter):
    def process(self, msg, kwargs):
        extra = {}
        extra.update(self.extra)

        if 'extra' in kwargs:
            extra.update(kwargs.pop('extra'))

        for name in list(kwargs.keys()):
            if name == 'exc_info':
                continue
            extra[name] = kwargs.pop(name)

        extra['extra_keys'] = list(sorted(extra.keys()))
        kwargs['extra'] = extra

        resource = kwargs['extra'].get('resource', None)
        if resource:
            if not resource.get('name', None):
                resource_type = resource.get('type', None)
                resource_id = resource.get('id', None)

                if resource_type and resource_id:
                    kwargs['extra']['resource'] = (
                            '[' + resource_type + '-' + resource_id + ']')

            else:
                kwargs['extra']['resource'] = (
                        '[' + resource.get('name', '') + ']')

        return msg, kwargs


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
    if getattr(context, 'to_dict', None):
        return context.to_dict()
    elif isinstance(context, dict):
        return context

    return {}


def _update_record_with_context(record):
    """Given a log record, update it with context information.

    The request context, if there is one, will either be passed with the
    incoming record or in the global thread-local store.
    """

    context = record.__dict__.get('context', get_current())
    if context:
        d = _dictify_context(context)
        for k, v in d.items():
            setattr(record, k, v)

    return context


_loggers = {}


def getLogger(name=None, project='unknown', version='unknown'):
    if name not in _loggers:
        _loggers[name] = KeywordArgumentAdapter(logging.getLogger(name), {
            'project': project,
            'version': version
        })

    return _loggers[name]


def setup(conf, version='unknown'):
    log_root = getLogger().logger

    for handler in list(log_root.handlers):
        log_root.removeHandler(handler)

    logpath = _get_log_file_path(conf)

    if logpath:
        rotating_conf = conf.rotating_filehandler
        rotating_conf.pop('filepath')
        rotating_conf['filename'] = logpath
        file_handler = logging.handlers.RotatingFileHandler(**rotating_conf)

        log_root.addHandler(file_handler)

    streamlog = logging.StreamHandler()
    log_root.addHandler(streamlog)

    for handler in log_root.handlers:
        handler.setFormatter(
            ContextFormatter(version=version,
                             datefmt=conf.date_format,
                             config=conf))

    log_root.setLevel(getLevelName(conf.level))


def _get_log_file_path(conf):
    rotating = conf.rotating_filehandler
    logfile = rotating['filename']
    logdir = rotating['filepath']

    if logfile and not logdir:
        return logfile

    if logfile and logdir:
        return os.path.join(logdir, logfile)

    if logdir:
        binary = os.path.basename(
            inspect.stack()[-1][1])  # get current file name
        return '%s.log' % (os.path.join(logdir, binary),)
    return None
