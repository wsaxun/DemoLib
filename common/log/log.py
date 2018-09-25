import os
import logging
import logging.handlers
from logging import getLevelName
import inspect
from common.log import formatters


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
            formatters.ContextFormatter(version=version,
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
