from django.contrib import admin

from .models import CeleryTask

# Register your models here.

class CeleryTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'task_id', 'state', 'created')
    list_filter = ('name', 'state')
    readonly_fields = ('name', 'task_id', 'created')
    fields = ['name', 'task_id', 'created', 'state', 'queue', '_args', '_kwargs', '_extra']
    actions = ['retry_task']

    def retry_task(self, request, queryset):
      for task in queryset:
        task.retry_task()
      self.message_user(request, "{} tasks have been re-queued.".format(len(queryset)))
    retry_task.short_description = 'Retry Selected Tasks'


admin.site.register(CeleryTask, CeleryTaskAdmin)
