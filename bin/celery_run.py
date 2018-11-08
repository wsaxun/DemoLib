import os
import sys

DEMOLIB_HOME = os.environ.get('DEMOLIB_HOME', '/home/greene/Github/DemoLib')
sys.path.append(DEMOLIB_HOME)

from celerydemo.app import celery_app
