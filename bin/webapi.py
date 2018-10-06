import os
import sys
from flask_script import Manager,Server
from werkzeug.wsgi import DispatcherMiddleware
from collections import OrderedDict

app_root = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(app_root, '../'))
sys.path.append(os.path.join(app_root, '../flaskdemo'))

from flaskdemo.webapi import create_app

def main():
    api_application = create_app()

    api_application.wsgi_app = DispatcherMiddleware(api_application.wsgi_app,
                                                    OrderedDict({
                                                        '/api': api_application
                                                    }))

    manage = Manager(api_application)
    manage.add_command('run',Server(host='0.0.0.0',port=8000))

    manage.run()

if __name__ == '__main__':
    main()
