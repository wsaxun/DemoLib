import pytest
import json
from mock import MagicMock
from collections import OrderedDict
from werkzeug.wsgi import DispatcherMiddleware

from flaskdemo.webapi import create_app
from flaskdemo.webapi.v1 import view

URL_TEST_INDEX = '/api/v1/'
URL_TEST_POLICY = '/api/v1/policy'
URL_TEST_RESULT = '/api/v1/result/c67f957adbae41fc98bc5dd8cb8e1a6c'

TASK_RESPONSE_DATA = b'{"task_id": "c67f957adbae41fc98bc5dd8cb8e1a6c"}'
TASK_RESULT_DATA = b'{"result": "data"}'

MOCK_TASK_RESPONSE_DATA = {"task_id": "c67f957adbae41fc98bc5dd8cb8e1a6c"}
MOCK_TASK_RESULT_DATA = {"result": "data"}


@pytest.fixture(scope="module")
def app():
    application = create_app()
    application.wsgi_app = DispatcherMiddleware(application.wsgi_app,
                                                OrderedDict({
                                                    '/api': application
                                                }))
    return application.test_client()


@pytest.fixture()
def task_data():
    rpc_response_data = MOCK_TASK_RESPONSE_DATA
    return MagicMock(return_value=json.dumps(rpc_response_data))


@pytest.fixture()
def task_result_data():
    rpc_response_data = MOCK_TASK_RESULT_DATA
    return MagicMock(return_value=json.dumps(rpc_response_data))


class TestWebApi(object):
    def test_index(self, app, task_data):
        url = URL_TEST_INDEX
        view.rpc_request = task_data

        get_response = app.get(url)

        # assert get_response.status_code == 200
        assert get_response.data == TASK_RESPONSE_DATA

    def test_policy(self, app, task_data):
        url = URL_TEST_POLICY

        view.rpc_request = task_data

        post_response = app.post(url)
        delete_response = app.delete(url)

        assert post_response.data == TASK_RESPONSE_DATA
        assert delete_response.data == TASK_RESPONSE_DATA

    def test_result(self, app, task_result_data):
        url = URL_TEST_RESULT
        view.rpc_request = task_result_data

        get_response = app.get(url)

        assert get_response.data == TASK_RESULT_DATA
