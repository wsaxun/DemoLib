from celery import Celery
from celery_config import config as CONFIG

celery_app = Celery('demo')
celery_app.config_from_object(CONFIG)  # 导入配置
