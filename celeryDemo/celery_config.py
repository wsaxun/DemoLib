from datetime import timedelta


class BaseConfig(object):
    # 使用rabbitmq作为消息代理
    # broker_url = 'amqp://username:password@127.0.0.1:5672/'
    broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/1'  # 任务结果存入redis
    task_serializer = 'msgpack'  # 任务序列化和反序列化使用msgpack方案
    result_serializer = 'json'  # 读取任务结果要求性能不高，使用可读性更好的JSON
    result_expires = 60 * 60 * 24  # 任务任务过期时间
    accept_content = ['json', 'msgpack']  # 指点接受的内容类型
    timezone = 'UTC'  # 设置时区
    enable_utc = True  # 开启utc
    imports = ['celery_tasks']  # 导入任务模块
    task_track_started = True  # 任务跟踪
    beat_schedule = {
        'test': {
            'task': 'celery_tasks.test_task_async',
            'schedule': timedelta(seconds=10),
        }
    }


class DevConfig(BaseConfig):
    pass


config = DevConfig()
