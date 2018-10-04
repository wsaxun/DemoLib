from celery_app import celery_app


@celery_app.task
def test_task_async():
    return 'result info.'
