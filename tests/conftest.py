import os
import sys
import pytest
import json
import mock
from collections import OrderedDict
from werkzeug.wsgi import DispatcherMiddleware

app_root = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(app_root, '../'))
sys.path.append(os.path.join(app_root, '../FlaskDemo'))

from web_api import create_app

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


@pytest.fixture(scope="module")
def task_data():
    rpc_response_data = MOCK_TASK_RESPONSE_DATA
    return mock.Mock(return_value=json.dumps(rpc_response_data))


@pytest.fixture(scope="module")
def task_result_data():
    rpc_response_data = MOCK_TASK_RESULT_DATA
    return mock.Mock(return_value=json.dumps(rpc_response_data))
