from functools import wraps

from apscheduler.job import Job
from namekodemo.schedule.schedulerConfig import misfire


def _inner_check_single(job_data, job, status):
    job_result = {'status': status}
    next_run_time = None
    if isinstance(job_data, job):
        if job_data.next_run_time:
            next_run_time = job_data.next_run_time.strftime(
                '%Y-%m-%d %H:%M:%S')
        job = dict(job_id=job_data.id,
                   func=job_data.func.__name__,
                   args=job_data.args,
                   kwargs=job_data.kwargs,
                   misfire_grace_time=job_data.misfire_grace_time,
                   next_run_time=next_run_time)
        job_result.update(data=job)
        return job_result
    return None


def _inner_check_list(job_data, status):
    job_result = {'status': status}
    next_run_time = None
    for one_job in job_data:
        serializer_data = []
        if isinstance(one_job, Job):
            if one_job.next_run_time:
                next_run_time = one_job.next_run_time.strftime(
                    '%Y-%m-%d %H:%M:%S')
            job = dict(job_id=one_job.id,
                       func=one_job.func.__name__,
                       args=one_job.args,
                       kwargs=one_job.kwargs,
                       misfire_grace_time=one_job.misfire_grace_time,
                       next_run_time=next_run_time)
            serializer_data.append(job)
        else:
            serializer_data.append(one_job)
            job_result.update(data=serializer_data)
    return job_result


def serialization(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        def serialization_one_job_or_job_list(job_data, status):
            ret = _inner_check_single(job_data, Job, status)
            if ret:
                return ret
            item = _inner_check_list(job_data, status)
            return item

        result = func(self, *args, **kwargs)
        if result['status'] == 'fail' or result['status'] != 'success':
            new_result = result
            return new_result
        if not result['data']:
            new_result = dict(status=result['status'])
        elif isinstance(result['data'], list) or isinstance(result['data'],
                                                            Job):
            new_result = serialization_one_job_or_job_list(result['data'],
                                                           result['status'])
            return new_result
        else:
            new_result = result
        return new_result

    return inner


def check_start_backup_param(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if not args:
            return {'status': 'fail', 'msg': 'position args is null'}
        if not kwargs.get('duration'):
            return {'status': 'fail', 'msg': 'not duration args'}
        if not kwargs.get('start_time'):
            return {'status': 'fail', 'msg': 'not start_time args'}
        if not kwargs.get('cron'):
            return {'status': 'fail', 'msg': 'not cron args'}
        # TODO
        misfire_grace_time = kwargs.get('misfire_grace_time')
        if not misfire_grace_time:
            misfire_grace_time = int(misfire * 60 * 60 * 24)
        kwargs['misfire_grace_time'] = misfire_grace_time
        result = func(self, *args, **kwargs)
        return result

    return inner
