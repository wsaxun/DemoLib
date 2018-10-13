import pytest
from mock import MagicMock
from nameko.testing.utils import get_container
from nameko.testing.services import entrypoint_hook

from namekodemo.taskservice import dependencies
from namekodemo.taskservice.service import TaskService
from common import conf
from namekodemo.taskservice.api import (
    fibonacci,
    add_policy,
    delete_policy
)

MOCK_TASK_ID = 'c67f957adbae41fc98bc5dd8cb8e1a6c'

AMQP_URI = {'AMQP_URI':'amqp://dev:dev@localhost:5672/demolib'}

@pytest.fixture()
def rabbit_conf():
    conf.get_amqp_conf = MagicMock(return_value=AMQP_URI)
    amqp_uri = conf.get_amqp_conf()
    return amqp_uri


@pytest.fixture(scope="module")
def taskId():
    task_id = MOCK_TASK_ID
    return MagicMock(return_value=task_id)


class TestTaskService(object):

    def test_taskApi(self, runner_factory, rabbit_conf, taskId):
        runner = runner_factory(rabbit_conf, TaskService)
        dependencies.get_taskid = taskId

        container = get_container(runner, TaskService)

        with entrypoint_hook(container, "fibonacci") as fibonacci:
            assert fibonacci() == MOCK_TASK_ID

        with entrypoint_hook(container, "add_policy") as add_policy:
            assert add_policy(None) == MOCK_TASK_ID

        with entrypoint_hook(container, "delete_policy") as delete_policy:
            assert delete_policy(None) == MOCK_TASK_ID

        with entrypoint_hook(container, "get_result") as get_result:
            assert get_result(MOCK_TASK_ID) == None


class TestApi(object):
    def test_fibonacci(self):
        assert fibonacci() == 55

    def test_add_policy(self):
        params = {'msg': 'test'}
        assert add_policy(params) == params

    def test_delete_policy(self):
        params = {'msg': 'test'}
        assert delete_policy(params) == params
