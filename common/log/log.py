import os
import logging
import logging.handlers
from logging import getLevelName
from common.context import get_current
from common.conf import get_log_config


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


def _get_logger(name=None):
    if name not in _loggers:
        _loggers[name] = logging.getLogger(name)

    return _loggers[name]


def getLogger(name=None):
    return _get_logger(name)


def setup(name=None, sub_log_path=None):
    conf = get_log_config()

    logger = _get_logger(name)

    for handler in list(logger.handlers):
        logger.removeHandler(handler)

    logpath = _get_log_file_path(conf, sub_log_path)

    if logpath:
        rotating_conf = conf.rotating_filehandler
        rotating_conf.pop('filepath')
        rotating_conf['filename'] = logpath
        file_handler = logging.handlers.RotatingFileHandler(**rotating_conf)

        logger.addHandler(file_handler)

    streamlog = logging.StreamHandler()
    logger.addHandler(streamlog)

    for handler in logger.handlers:
        handler.setFormatter(ContextFormatter(datefmt=conf.date_format,
                                              config=conf))

    logger.setLevel(getLevelName(conf.level))


def _get_log_file_path(conf, sub_log_path):
    rotating = conf.rotating_filehandler
    logfile = rotating['filename']
    logdir = rotating['filepath']

    if sub_log_path:
        sub_path, file_name = os.path.split(sub_log_path)
        if sub_path:
            logdir = os.path.join(logdir, sub_path)
        if file_name:
            logfile = file_name

    if not os.path.exists(logdir):
        os.makedirs(logdir)

    if logfile and not logdir:
        return logfile

    if logfile and logdir:
        return os.path.join(logdir, logfile)
    return None
