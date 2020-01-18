from django.contrib import admin
from app.models import Task
from app.tasks import update_task_ctask


def handle_task_action(modeladmin, request, queryset):
    for task in queryset:
        update_task_ctask.delay(task.id)
handle_task_action.short_description = "Обработать"


class TaskAdmin(admin.ModelAdmin):
    list_display = ('func', 'image_tag', 'interval', 'dt', 'date')
    readonly_fields = ('date', 'result')
    actions = (handle_task_action, )
admin.site.register(Task, TaskAdmin)
