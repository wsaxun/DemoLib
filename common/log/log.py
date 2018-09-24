import os
import logging
import logging.handlers
from common.log import formatters, handlers as custom_handlers

TRACE = custom_handlers._TRACE


class BaseLoggerAdapter(logging.LoggerAdapter):
    warn = logging.LoggerAdapter.warning

    @property
    def handlers(self):
        return self.logger.handlers

    def trace(self, msg, *args, **kwargs):
        self.log(TRACE, msg, *args, **kwargs)


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
    # if name and name.startswitch('oslo_'):
    #     name = 'oslo.' + name[5:]
    if name not in _loggers:
        _loggers[name] = KeywordArgumentAdapter(logging.getLogger(name), {
            'project': project,
            'version': version
        })

    return _loggers[name]


def setup(conf,product_name,version='unknown'):
    _setup_logging_from_conf(conf,product_name,version)

def _get_log_file_path(conf, binary=None):
    logfile = conf.log_file
    logdir = conf.log_dir

    if logfile and not logdir:
        return logfile

    if logfile and logdir:
        return os.path.join(logdir, logfile)

    if logdir:
        binary = binary or custom_handlers._get_binary_name()
        return '%s.log' % (os.path.join(logdir, binary),)
    return None


def _setup_logging_from_conf(conf, project, version):
    log_root = getLogger().logger

    for handler in list(log_root.handlers):
        log_root.removeHandler(handler)

    logpath = _get_log_file_path(conf)

    if logpath:
        file_handler = logging.handlers.RotatingFileHandler
        filelog = file_handler(logpath)
        log_root.addHandler(filelog)

    streamlog = custom_handlers.ColorHandler()
    log_root.addHandler(streamlog)

    datefmt = conf.log_date_format

    for handler in log_root.handlers:
        handler.setFormatter(
            formatters.ContextFormatter(project=project, version=version,
                                        datefmt=datefmt, config=conf))

    _refresh_root_level(conf.debug)


def _refresh_root_level(debug):
    """Set the level of the root logger.

    :param debug: If 'debug' is True, the level will be DEBUG.
     Otherwise the level will be INFO.
    """
    log_root = getLogger().logger
    if debug:
        log_root.setLevel(logging.DEBUG)
    else:
        log_root.setLevel(logging.INFO)

