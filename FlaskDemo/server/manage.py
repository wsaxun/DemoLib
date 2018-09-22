import sys

sys.path.append('../')

from flask_script import Manager
from collections import OrderedDict
from werkzeug.wsgi import DispatcherMiddleware
from FlaskDemo.server.application import api, admin

api.wsgi_app = DispatcherMiddleware(api.wsgi_app,OrderedDict({
    '/api':api,
}))

application = Manager(api)

if __name__ == '__main__':
    application.run()
