from common.log import log as logging

from other.other import func as func1
from other.other2 import func as func2

import uuid
import sys

sys.path.append('../')

LOG = logging.getLogger(__name__)
DOMAIN = 'demo'


def generate_request_id():
    return uuid.uuid4().hex


if __name__ == '__main__':
    logging.setup(name=__name__, sub_log_path='logtest/test.log')

    LOG.info("Welcome to Logging")
    LOG.info("Without context")

    logger1 = LOG
    func1()

    logger2 = LOG
    LOG.info("setup after")

    func2()

    LOG.info("setup 2 after")
