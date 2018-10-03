import os
import sys
from flask_script import Manager
from werkzeug.wsgi import DispatcherMiddleware
from collections import OrderedDict

app_root = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(app_root, '../'))
sys.path.append(os.path.join(app_root, '../FlaskDemo'))

from web_api import create_app

api_application = create_app()

api_application.wsgi_app = DispatcherMiddleware(api_application.wsgi_app,
                                                OrderedDict({
                                                    '/api': api_application
                                                }))

manage = Manager(api_application)

if __name__ == '__main__':
    manage.run()
