import json

from celery import signature
from celery.states import PENDING, RETRY
from django.db import models

# Create your models here.
class CeleryTask(models.Model):
    name = models.TextField()
    queue = models.TextField(null=True, blank=True)
    task_id = models.UUIDField()
    state = models.CharField(max_length=25, default=PENDING)
    created = models.DateTimeField(auto_now_add=True)
    _args = models.TextField(null=True, blank=True)
    _kwargs = models.TextField(null=True, blank=True)
    _extra = models.TextField(null=True, blank=True)

    def retry_task(self):
        # resend task
        args = self.args
        kwargs = self.kwargs
        params = {}
        if args:
            params['args'] = args
        if kwargs:
            params['kwargs'] = kwargs
        print('params are', params)
        signature(
            self.name,
            **params
        ).apply_async(queue=self.queue or None)
        self.state = RETRY
        self.save()

    def __str__(self):
        return str(self.task_id)

    def __unicode__(self):
        return self.__str__()

    @property
    def args(self):
        return json.loads(self._args or 'null')

    @args.setter
    def args(self, value):
        self._args = json.dumps(value)

    @property
    def kwargs(self):
        return json.loads(self._kwargs or 'null')

    @kwargs.setter
    def kwargs(self, value):
        self._kwargs = json.dumps(value)

    @property
    def extra(self):
        return json.loads(self._extra or 'null')

    @extra.setter
    def extra(self, value):
        self._extra = json.dumps(value)
