
from common.log import log as logging
from collections import namedtuple

from other.other import func as func1
from other.other2 import func as func2

import uuid
import sys
sys.path.append('../')

LOG = logging.getLogger(__name__)
DOMAIN = 'demo'

def generate_request_id():
    return uuid.uuid4().hex

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

if __name__ == '__main__':
    logging.setup(CONF,sub_log_path='logtest/test.log')

    LOG.info("Welcome to Logging")
    LOG.info("Without context")

    logger1 = LOG
    func1()

    logger2 = LOG
    LOG.info("setup after")

    func2()

    LOG.info("setup 2 after")
