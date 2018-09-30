from collections import namedtuple

__all__ = ['CONF']

Cfg = namedtuple('cfg', [
    'date_format',
    'level',
    'default_format_string',
    'context_format_string',
    'rotating_filehandler',
])

CONF = Cfg(
    date_format='%Y-%m-%d %H:%M:%S',
    level='INFO',
    default_format_string='%(asctime)s %(process)d %(levelname)s %(name)s %(message)s',
    context_format_string='%(asctime)s %(process)d %(levelname)s %(name)s [%(request_id)s] %(message)s',
    rotating_filehandler={
        'filename':'base.log',
        # 'context_filename':'context_file.log',
        'filepath':'/home/greene/Github/DemoLib/log',
        'maxBytes':104857600,
        'backupCount':1000,
        'encoding':'utf8'
    }
)

def get_log_config():
    return CONF