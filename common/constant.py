import os

APP_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../')

DEMOLIB_HOME = os.environ.get('DEMOLIB_HOME', APP_ROOT)
DEMOLIB_CURRENT_ENV = os.environ.get('DEMOLIB_CURRENT_ENV', 'DEV')
