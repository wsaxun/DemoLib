from celery.signals import (
    before_task_publish,
    after_task_publish,
    task_prerun,
    task_postrun,
    task_retry,
    task_success,
    task_failure,
    task_revoked
)

@before_task_publish.connect
def before_task_publish_signal(**kwargs):
    print('[SIGNALS] before_task_publish_signal')

@after_task_publish.connect
def after_task_publish_signal(**kwargs):
    print('[SIGNALS] after_task_publish_signal')

@task_prerun.connect
def task_prerun_signal(task_id=None,sender=None,args=None,**kwargs):
    print('[SIGNALS] task_prerun_signal')

@task_postrun.connect
def task_postrun_signal(**kwargs):
    print('[SIGNALS] task_postrun_signal')

@task_retry.connect
def task_retry_signal(**kwargs):
    print('[SIGNALS] task_retry_signal')

@task_success.connect
def task_success_signal(**kwargs):
    print('[SIGNALS] task_success_signal')

@task_failure.connect
def task_failure_signal(**kwargs):
    print('[SIGNALS] task_failure_signal')

@task_revoked.connect
def task_revoked_signal(**kwargs):
    print('[SIGNALS] task_revoked_signal')

