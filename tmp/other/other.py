import uuid
from common.log import log as logging
from common.context import RequestContext

LOG = logging.getLogger(__name__)

logging.setup(name=__name__, sub_log_path='other/other.log')


def func():
    request_id = uuid.uuid4().hex
    tenent_id = '10000'
    RequestContext(request_id=request_id, project_id=tenent_id)
    LOG.info("With context")
