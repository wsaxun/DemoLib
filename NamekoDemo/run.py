from __future__ import print_function

import sys

sys.path.append('../')

import eventlet

eventlet.monkey_patch()  # noqa (code before rest of imports)

import errno
import signal

from eventlet import backdoor

from nameko.runners import ServiceRunner
from collections import namedtuple

# from timemachine.common import log as logging
from common.log import log as logging
from NamekoDemo.service import TaskService

LOG = logging.getLogger(__name__)

DOMAIN = 'demo'


def setup_backdoor(runner, port):
    def _bad_call():
        raise RuntimeError(
            'This would kill your service, not close the backdoor. To exit, '
            'use ctrl-c.')

    socket = eventlet.listen(('localhost', port))
    # work around https://github.com/celery/kombu/issues/838
    socket.settimeout(None)
    gt = eventlet.spawn(
        backdoor.backdoor_server,
        socket,
        locals={
            'runner': runner,
            'quit': _bad_call,
            'exit': _bad_call,
        })
    return socket, gt


def run(services, config, backdoor_port=None):
    service_runner = ServiceRunner(config)
    for service_cls in services:
        service_runner.add_service(service_cls)

    def shutdown(signum, frame):
        # signal handlers are run by the MAINLOOP and cannot use eventlet
        # primitives, so we have to call `stop` in a greenlet
        eventlet.spawn_n(service_runner.stop)

    signal.signal(signal.SIGTERM, shutdown)

    if backdoor_port is not None:
        setup_backdoor(service_runner, backdoor_port)

    service_runner.start()

    # if the signal handler fires while eventlet is waiting on a socket,
    # the __main__ greenlet gets an OSError(4) "Interrupted system call".
    # This is a side-effect of the eventlet hub mechanism. To protect nameko
    # from seeing the exception, we wrap the runner.wait call in a greenlet
    # spawned here, so that we can catch (and silence) the exception.
    runnlet = eventlet.spawn(service_runner.wait)

    while True:
        try:
            runnlet.wait()
        except OSError as exc:
            LOG.info('OSERROR.')
            if exc.errno == errno.EINTR:
                LOG.info('ERRNO EINTR.')
                # this is the OSError(4) caused by the signalhandler.
                # ignore and go back to waiting on the runner
                continue
            raise
        except KeyboardInterrupt:
            print()  # looks nicer with the ^C e.g. bash prints in the terminal
            try:
                service_runner.stop()
                LOG.info('SERVICE RUNNER STOP!')
            except KeyboardInterrupt:
                print()  # as above
                LOG.info('SERVICE RUNNER KILLED!')
                service_runner.kill()
        else:
            # runner.wait completed
            LOG.info('RUNNER WAIT COMPLETED.')
            break


def main():
    # config = get_amqp_config()
    config = {'AMQP_URI': 'amqp://guest:guest@localhost:5672'}

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
        default_format_string='%(asctime)s %(process)d %(thread)d %(levelname)s %(name)s %(instance)s%(message)s',
        context_format_string='%(asctime)s %(process)d %(thread)d %(levelname)s %(name)s [%(request_id)s] %(message)s',
        rotating_filehandler={
            'filename': 'timemachine-efs.log',
            'filepath': '/home/greene/Github/DemoLib/log',
            'maxBytes': 104857600,
            'backupCount': 1000,
            'encoding': 'utf8'
        }
    )

    logging.setup(CONF)

    # context.RequestContext(tenant_id='d6134462', request_id=None, domain=DOMAIN)

    services = []
    services.append(TaskService)

    run(services, config)


if __name__ == '__main__':
    main()
