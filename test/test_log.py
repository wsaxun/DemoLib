from collections import namedtuple
from common.log import log as logging
from common.context import RequestContext

import uuid
import sys
sys.path.append('../')

LOG = logging.getLogger(__name__)
DOMAIN = 'demo'

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
    default_format_string='%(asctime)s %(process)d %(levelname)s %(name)s %(instance)s%(message)s',
    context_format_string='%(asctime)s %(process)d %(levelname)s %(name)s [%(request_id)s] %(message)s',
    rotating_filehandler={
        'filename':'timemachine-efs.log',
        'filepath':'/home/greene/Github/DemoLib/log',
        'maxBytes':104857600,
        'backupCount':1000,
        'encoding':'utf8'
    }
)

def generate_request_id():
    return uuid.uuid4().hex

if __name__ == '__main__':
    logging.setup(CONF)

    LOG.info("Welcome to Logging")
    LOG.info("Without context")

    request_id = generate_request_id()
    tenent_id = '10000'
    RequestContext(request_id=request_id,project_id=tenent_id)

    LOG.info("With context")
