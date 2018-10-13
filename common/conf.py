import os
import yaml
from collections import namedtuple

APP_HOME = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../')
CURRENT_ENV = 'DEV'


def _load_yaml_config(file_name):
    with open(os.path.join(APP_HOME, file_name)) as fp:
        conf = yaml.load(fp.read())
    return conf


def get_log_conf():
    conf = _load_yaml_config('etc/log.yaml')

    Log = namedtuple('log', [
        'date_format',
        'level',
        'default_format_string',
        'context_format_string',
        'rotating_filehandler',
    ])

    CONF = Log(
        date_format=conf['date_format'],
        level=conf['level'],
        default_format_string=conf['default_format_string'],
        context_format_string=conf['context_format_string'],
        rotating_filehandler=conf['rotating_filehandler']
    )
    CONF.rotating_filehandler['filepath'] = os.path.join(APP_HOME, 'log')
    return CONF


def get_webApi_conf():
    conf = _load_yaml_config('etc/webApi.yaml')
    return conf[CURRENT_ENV]


def get_amqp_conf():
    conf = _load_yaml_config('etc/main.yaml')
    return {'AMQP_URI': conf[CURRENT_ENV]['AMQP_URI']}


def get_db_uri():
    conf = _load_yaml_config('etc/main.yaml')
    return {'DB_URI': conf[CURRENT_ENV]['DB_URI']}
