import uuid
from celerydemo.app import celery_app
from common.log import log as logging
from common.context import RequestContext

LOG = logging.getLogger(__name__)

@celery_app.task
def beats_task_async():
    RequestContext(uuid.uuid4().hex, '10000')

    LOG.info('beat_task info')
    return 'beat result info.'

@celery_app.task
def task_async():
    RequestContext(uuid.uuid4().hex,'10000')

    LOG.info('task info')
    return 'task result info'
