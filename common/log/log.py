import sys
import os
import logging
import logging.handlers
from logging import getLevelName
import inspect
import datetime
from dateutil import tz
from common.context import get_current



class ContextFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        self.conf = kwargs.pop('config', None)
        logging.Formatter.__init__(self, *args, **kwargs)

    def format(self, record):
        _update_record_with_context(record)

        if record.__dict__.get('request_id'):
            fmt = self.conf.context_format_string
        else:
            fmt = self.conf.default_format_string

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
        context_dict = dict()
        if getattr(context, 'to_dict', None):
            context_dict = context.to_dict()
        elif isinstance(context, dict):
            context_dict = context

        for k, v in context_dict.items():
            setattr(record, k, v)

    return context


_loggers = {}


def getLogger(name=None):
    if name not in _loggers:
        _loggers[name] = logging.getLogger(name)

    return _loggers[name]


def setup(conf,logger=None):

    log_root = getLogger()

    if logger:
        log_root = logger

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
        handler.setFormatter(ContextFormatter(datefmt=conf.date_format,
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
