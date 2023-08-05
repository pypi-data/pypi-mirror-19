from celery import signature
from celery.signals import task_failure, task_postrun, task_prerun
from celery.states import FAILURE

from . import conf

# Task status tracking
@task_prerun.connect
def track_task_prerun(sender=None, **kwargs):
    task_id = kwargs.get('task_id')
    task_args = kwargs.get('args')
    task_kwargs = kwargs.get('kwargs')
    task_queue = sender.request.delivery_info.get('routing_key')
    signature(
      'celery_aide.tasks.task_update',
      kwargs={
        'task_id': task_id,
        'task_args': task_args,
        'task_kwargs': task_kwargs,
        'task_name': sender.name,
        'task_queue': task_queue,
      },
      queue=conf.CELERY_AIDE_QUEUE
    ).apply_async()

@task_postrun.connect
def track_task_postrun(sender=None, **kwargs):
    task_id = kwargs.get('task_id')
    task_args = kwargs.get('args')
    task_kwargs = kwargs.get('kwargs')
    task_state = kwargs.get('state')
    signature(
      'celery_aide.tasks.task_update',
      kwargs={
        'task_id': task_id,
        'task_args': task_args,
        'task_kwargs': task_kwargs,
        'task_name': sender.name,
        'task_state': task_state,
      },
      queue=conf.CELERY_AIDE_QUEUE
    ).apply_async()

@task_failure.connect
def track_task_failure(sender=None, **kwargs):
    task_id = kwargs.get('task_id')
    task_args = kwargs.get('args')
    task_kwargs = kwargs.get('kwargs')
    task_traceback = kwargs.get('traceback')
    if task_traceback:
        import traceback
        task_extra = {'traceback': '\n'.join(traceback.format_tb(task_traceback))}
    else:
        task_extra = None

    signature(
      'celery_aide.tasks.task_update',
      kwargs={
        'task_id': task_id,
        'task_args': task_args,
        'task_extra': task_extra,
        'task_kwargs': task_kwargs,
        'task_name': sender.name,
        'task_state': FAILURE,
      },
      queue=conf.CELERY_AIDE_QUEUE
    ).apply_async()
