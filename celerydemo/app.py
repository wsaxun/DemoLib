import os
import sys
from celery import Celery
from config import config as CONFIG

DEMOLIB_HOME = os.environ.get('DEMOLIB_HOME', '/home/greene/Github/DemoLib')
sys.path.append(DEMOLIB_HOME)

from common.log import log as logging

logging.setup(sub_log_path='celery.log')

LOG = logging.getLogger(__name__)

LOG.info('init LOGGER')

celery_app = Celery('demo')
celery_app.config_from_object(CONFIG)  # 导入配置
