import eventlet

eventlet.monkey_patch()

import uuid
from eventlet.event import Event
from nameko.extensions import DependencyProvider

from common.log import log as logging
from taskService.api import (
    fibonacci,

    add_policy,
    delete_policy
)

LOG = logging.getLogger(__name__)


class TaskProcessor(DependencyProvider):

    def __init__(self):
        self.tasks = {
            'fibonacci': fibonacci,

            'add_policy': add_policy,
            'delete_policy': delete_policy
        }
        self.results = {}

    def start_task(self, name, *args, **kwargs):
        task_id = uuid.uuid4().hex
        task = self.tasks.get(name)

        event = Event()
        gt = self.container.spawn_managed_thread(lambda: task(*args, **kwargs))
        gt.link(lambda res: event.send(res.wait()))

        self.results[task_id] = event
        return task_id

    def get_result(self, task_id):

        LOG.info('get task %s result' % task_id)

        result = self.results.get(task_id)

        if result is None:
            res = "missing"
        elif result.ready():
            res = result.wait()
        else:
            res = "pending"

        return res

    def get_dependency(self, worker_ctx):

        class TaskApi(object):
            start_task = self.start_task
            get_result = self.get_result

        task_api = TaskApi()
        return task_api
