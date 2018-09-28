import sys
import pytest
import mock

sys.path.append('../')

from FlaskDemo.app import app as application




@pytest.fixture(scope="module")
def client():
    app = application
    return app.test_client()

@pytest.fixture(scope="module")
def index_data():
    response_data = {"msg":"test info."}
    return mock.Mock(return_value=response_data)
