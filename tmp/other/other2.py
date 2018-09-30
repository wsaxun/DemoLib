import uuid
from common.log import log as logging
from common.context import RequestContext
from collections import namedtuple


LOG = logging.getLogger(__name__)

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

logging.setup(CONF,sub_log_path='other2/other2.log')

def func():
    request_id = uuid.uuid4().hex
    tenent_id = '10000'
    # RequestContext(request_id=request_id,project_id=tenent_id)
    LOG.info("With context")
