import uuid

import eventlet
from eventlet.event import Event
from nameko.rpc import rpc
from nameko.extensions import DependencyProvider

from common.log import log as logging
from common.context import RequestContext

LOG = logging.getLogger(__name__)


# a simple task
def fibonacci(n,context):
    # RequestContext(request_id=uuid.uuid4().hex, project_id='10000')
    a, b = 1, 1
    LOG.info('fib')
    eventlet.sleep(10)
    for i in range(n-1):
        a, b = b, a+b
        if n % 50 == 0:
            eventlet.sleep()  # won't yield voluntarily since there's no i/o
    LOG.info('fib end.')
    return a


class TaskProcessor(DependencyProvider):

    def __init__(self):
        self.tasks = {
            'fibonacci': fibonacci
            # add other tasks here
        }
        self.results = {}

    def start_task(self, name, n,context):
        # generate unique id
        task_id = uuid.uuid4().hex

        # get the named task
        task = self.tasks.get(name)

        LOG.info('DependencyProvider start_task.')

        # execute it in a container thread and send the result to an Event
        event = Event()
        gt = self.container.spawn_managed_thread(lambda: task(n,context))
        gt.link(lambda res: event.send(res.wait()))

        # store the Event and return the task's unique id to the caller
        self.results[task_id] = event
        return task_id

    def get_result(self, task_id):
        # get the result Event for `task_id`
        result = self.results.get(task_id)
        if result is None:
            return "missing"
        # if the Event is ready, return its value
        if result.ready():
            return result.wait()
        return "pending"

    def get_dependency(self, worker_ctx):

        class TaskApi(object):
            start_task = self.start_task
            get_result = self.get_result

        return TaskApi()


class TaskService(object):
    name = "tasks"

    processor = TaskProcessor()

    @rpc
    def start_task(self, name, n):

        context = RequestContext(request_id=uuid.uuid4().hex,project_id='10000')

        LOG.info('task start.')
        result = self.processor.start_task(name,n,context)
        LOG.info('task end.')
        return result

    @rpc
    def get_result(self, task_id):
        return self.processor.get_result(task_id)
