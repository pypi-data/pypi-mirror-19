from celery import Celery
from celery.states import state, PENDING

from .models import CeleryTask

app = Celery('celery_aide')

@app.task
def task_update(task_id=None, task_args=None, task_extra=None, task_kwargs=None, task_name=None, task_queue=None, task_state=None):
  task, created = CeleryTask.objects.get_or_create(task_id=task_id)
  if not created:
      # if we are not the first one here, we only want to update if we are at a state with higher precedence
      if state(task_state) < state(task.state):
          if task.queue is None and task_queue is not None:
              task.queue = task_queue
              task.save()
          return
  task.args = task_args
  task.extra = task_extra
  task.kwargs = task_kwargs
  task.name = task_name
  if task_queue:
      task.queue = task_queue
  task.state = task_state or PENDING
  task.save()
