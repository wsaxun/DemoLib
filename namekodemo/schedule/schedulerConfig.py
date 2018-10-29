from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from common.conf import get_schedule

__conf = get_schedule()

job_stores = {'default': SQLAlchemyJobStore(url=__conf['DBURL'])}
executors = {'default': ThreadPoolExecutor(__conf['EXECUTOR']), }
job_defaults = {'coalesce': __conf['COALESCE'],
                'max_instances': __conf['MAXINSTANCES']}

# 100%
misfire = __conf['MISFIRE']

# start_backup url
# start_backup_url = 'https://www.httpbin.org/post'
start_backup_url = __conf['TASKAPI']

# request timeout
request_timeout = __conf['TIMEOUT']
