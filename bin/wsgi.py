import os
import sys
from collections import OrderedDict
from werkzeug.wsgi import DispatcherMiddleware

sys.path.append(os.environ.get('DEMOLIB_HOME'))

from flaskdemo.webapi import create_app

application = create_app()

application.wsgi_app = DispatcherMiddleware(application.wsgi_app, OrderedDict((
    ('/api', application),
)))
