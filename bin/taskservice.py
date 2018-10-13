from __future__ import print_function

import eventlet

eventlet.monkey_patch()  # noqa (code before rest of imports)

import os
import sys
import errno
import signal

from eventlet import backdoor

from nameko.runners import ServiceRunner

sys.path.append(os.environ.get('DEMOLIB_HOME',None))

from common.conf import get_amqp_conf
from common.log import log as logging

LOG = logging.getLogger(__name__)


def run(services, config):
    service_runner = ServiceRunner(config)
    for service_cls in services:
        service_runner.add_service(service_cls)

    def shutdown(signum, frame):
        # signal handlers are run by the MAINLOOP and cannot use eventlet
        # primitives, so we have to call `stop` in a greenlet
        eventlet.spawn_n(service_runner.stop)

    signal.signal(signal.SIGTERM, shutdown)

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
            if exc.errno == errno.EINTR:
                # this is the OSError(4) caused by the signalhandler.
                # ignore and go back to waiting on the runner
                continue
            raise
        except KeyboardInterrupt:
            print()  # looks nicer with the ^C e.g. bash prints in the terminal
            try:
                service_runner.stop()
            except KeyboardInterrupt:
                print()  # as above
                service_runner.kill()
        else:
            # runner.wait completed
            break


from namekodemo.taskservice.service import TaskService


def main():
    config = get_amqp_conf()
    logging.setup(sub_log_path='namekodemo/taskservice.log')

    services = []
    services.append(TaskService)

    run(services, config)


if __name__ == '__main__':
    main()
