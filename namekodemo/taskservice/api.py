import eventlet
import uuid

from common.log import log as logging
from common.context import RequestContext
from .models import Policy
from datetime import datetime

LOG = logging.getLogger(__name__)


def generate_request_id():
    return uuid.uuid4().hex


def fibonacci():
    """
    only test
    :param n:
    :return:
    """
    RequestContext(generate_request_id(), '100000')

    LOG.info('start test fibonacci.')

    n = int(10)
    a, b = 1, 1

    for i in range(n - 1):
        a, b = b, a + b
        if n % 50 == 0:
            eventlet.sleep()  # won't yield voluntarily since there's no i/o

    LOG.info('end test fibonacci.')
    return a


def add_policy(params):
    """
    add policy

    :param params:
    :return:
    """
    RequestContext(generate_request_id(), '100000')

    LOG.info('start add policy, params is %s' % params)

    # add other code

    policy = Policy()
    params['now_time'] = datetime.now()
    policy.insert(params)

    LOG.info('end add policy.')
    return params


def delete_policy(params):
    """
    delete policy

    :param params:
    :return:
    """
    RequestContext(generate_request_id(), '100000')

    LOG.info('start delete policy, params is %s' % params)

    # add other code

    LOG.info('end delete policy.')
    return params
