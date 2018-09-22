import sys

sys.path.append('../')


from collections import OrderedDict
from werkzeug.wsgi import DispatcherMiddleware
from FlaskDemo.server.application import api, admin


application = DispatcherMiddleware(None,OrderedDict({
    '/api':api,
    '/admin':admin,
}))
