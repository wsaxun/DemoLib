from celery import Celery
from celerydemo.config import config as CONFIG
from common.log import log as logging

logging.setup(sub_log_path='celery.log')

celery_app = Celery('demo')
celery_app.config_from_object(CONFIG)  # 导入配置
