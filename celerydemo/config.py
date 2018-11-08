from datetime import timedelta
from kombu import Queue
from celery.schedules import crontab

class BaseConfig(object):
    # 使用rabbitmq作为消息代理
    broker_url = 'amqp://guest:guest@localhost:5672/celery'
    # broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/1'  # 任务结果存入redis
    task_serializer = 'msgpack'  # 任务序列化和反序列化使用msgpack方案
    result_serializer = 'json'  # 读取任务结果要求性能不高，使用可读性更好的JSON
    result_expires = 60 * 60 * 24  # 任务任务过期时间
    accept_content = ['json', 'msgpack']  # 指点接受的内容类型
    timezone = 'UTC'  # 设置时区
    enable_utc = True  # 开启utc
    imports = ['celerydemo.tasks','celerydemo.task_signals']  # 导入任务模块
    task_track_started = True  # 任务跟踪
    # worker_hijack_root_logger = False # 禁用log root 清理

    beat_schedule = {
        'test': {
            'task': 'celerydemo.tasks.beats_task_async',
            # 'schedule': crontab('*')
            'schedule': timedelta(seconds=10),
        }
    }

    task_queues = (
        Queue('tasks',routing_key='tasks.#'),
        Queue('beats',routing_key='beats.#'),
    )

    task_default_exchange = 'celery'
    task_default_exchange_type = 'topic'
    task_default_routing_key = 'tasks.default'

    task_routes = {
        'celerydemo.tasks.beats_task_async':{
            'queue': 'beats',
            'routing_key': 'beats.test'
        }
    }

class DevConfig(BaseConfig):
    pass


config = DevConfig()
