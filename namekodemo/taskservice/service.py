from nameko.rpc import rpc

from common.log import log as logging
from namekodemo.taskservice.dependencies import TaskProcessor

LOG = logging.getLogger(__name__)


class TaskService(object):
    name = "task_service"
    processor = TaskProcessor()

    @rpc
    def fibonacci(self):
        name = 'fibonacci'
        return self.processor.start_task(name)

    @rpc
    def add_policy(self, params):
        name = 'add_policy'
        return self.processor.start_task(name, params)

    @rpc
    def delete_policy(self, params):
        name = 'delete_policy'
        return self.processor.start_task(name, params)

    @rpc
    def get_result(self, task_id):
        '''
        get task result
        :param task_id: task id
        :return: task id and result
        '''
        return self.processor.get_result(task_id)
