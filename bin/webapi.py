import os
import sys
from flask_script import Manager, Server
from werkzeug.wsgi import DispatcherMiddleware
from collections import OrderedDict

sys.path.append(os.environ.get('DEMOLIB_HOME', None))

from flaskdemo.webapi import create_app


def main():
    api_application = create_app()

    api_application.wsgi_app = DispatcherMiddleware(api_application.wsgi_app,
                                                    OrderedDict({
                                                        '/api': api_application
                                                    }))

    manage = Manager(api_application)
    manage.add_command('run', Server(host='0.0.0.0', port=8000))

    manage.run()


if __name__ == '__main__':
    main()
