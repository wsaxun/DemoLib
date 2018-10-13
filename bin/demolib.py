"""Usage:
  demolib.py [all]
  demolib.py [webapi]
  demolib.py [task]
  demolib.py [wsgi]

Arguments:
  all         start all service
  wsgi        use gunicorn to start wsgi.py
  webapi      debug for use webapi.py
  task        debug for use taskservice.py

Options:
  -h --help
  -a --webapi
  -w --wsgi
  -t --type
  -s --supervisord
"""

import os
import subprocess
from docopt import docopt

DEMOLIB_HOME = os.environ.get('DEMOLIB_HOME', None)


def supervisord():
    subprocess.call(['supervisord', '-c',
                     os.path.join(DEMOLIB_HOME, 'etc/supervisord.cfg')])


def webapi():
    subprocess.call(
        ['python', os.path.join(DEMOLIB_HOME, 'bin/webapi.py'), 'run'])


def taskservice():
    subprocess.call(
        ['python', os.path.join(DEMOLIB_HOME, 'bin/taskservice.py')])


def wsgi():
    subprocess.call(
        ['gunicorn', '-w', '3', 'wsgi:application', '-b', '0.0.0.0:8001'])


def main(args):
    if args.get('all', None):
        supervisord()
    elif args.get('webapi', None):
        webapi()
    elif args.get('task', None):
        taskservice()
    elif args.get('wsgi', None):
        wsgi()
    else:
        print(__doc__)


if __name__ == '__main__':
    args = docopt(__doc__, version='DemoLib 1.0')
    main(args)
