import os
import sys
import uuid
from celery.signals import task_prerun
from app import celery_app
from api import fibonacci,add_policy,delete_policy

DEMOLIB_HOME = os.environ.get('DEMOLIB_HOME', '/home/greene/Github/DemoLib')
sys.path.append(DEMOLIB_HOME)

from common.log import log as logging
from common.context import RequestContext

LOG = logging.getLogger(__name__)

@celery_app.task
def test_task_async():
    RequestContext(uuid.uuid4().hex, '100000')

    LOG.info('test_task info')
    return 'result info.'

@celery_app.task
def fibonacci_async():
    result = fibonacci()
    return result

@celery_app.task
def add_policy_async(params):
    result = add_policy(params)
    return result

@celery_app.task
def delete_policy_async(params):
    result = delete_policy(params)
    return result

@task_prerun.connect
def task_handler(task_id=None,sender=None,args=None,**kwargs):
    RequestContext(task_id, '10000')
