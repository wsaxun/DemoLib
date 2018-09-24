from collections import namedtuple
from common.log import log as logging
from common.log import context

import sys
sys.path.append('../')
from other import action

import eventlet
from eventlet.event import Event

LOG = logging.getLogger(__name__)
DOMAIN = 'demo'

Cfg = namedtuple('cfg', [
    'log_file',
    'log_dir',
    'log_date_format',
    'debug',
    'logging_default_format_string',
    'logging_context_format_string',
])

CONF = Cfg(
    log_file=None,
    log_dir=None,
    log_date_format='%Y-%m-%d %H:%M:%S',
    debug=False,
    logging_default_format_string='%(asctime)s %(process)d %(levelname)s %(name)s [-] %(instance)s%(message)s',
    logging_context_format_string='%(asctime)s %(process)d %(levelname)s %(name)s [%(request_id)s] %(instance)s%(message)s'
)


if __name__ == '__main__':
    logging.setup(CONF, DOMAIN)

    LOG.info("Welcome to Logging")
    LOG.info("Without context")

    context.RequestContext(tenant_id='d6134462', request_id=None, domain=DOMAIN)

    LOG.info("With context")


    action()
