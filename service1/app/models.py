from django.conf import settings
from django.db import models
from django.utils.html import escape
from django.utils.safestring import mark_safe


class Task(models.Model):
    FUNC_TYPE_DICT = {
        (1, 't + 2/t'),
        (2, 'sin(t)'),
    }
    func = models.PositiveIntegerField(choices=FUNC_TYPE_DICT, verbose_name='Функция')
    result = models.CharField(max_length=255, verbose_name='График')
    interval = models.PositiveIntegerField(verbose_name='Интервал t, дней')
    date = models.DateTimeField(null=True, verbose_name='Дата обработки')
    dt = models.PositiveIntegerField(verbose_name='Шаг t, часы')

    def image_tag(self):
        if 'img/' in self.result:
            content = mark_safe(f'<img src="{settings.MEDIA_URL}{self.result}" width="250"/>')
        else:
            content = escape(self.result)
        return content

    image_tag.short_description = 'Результат'

    def save(self, *args, **kwargs):
        need_update = not self.id
        super(Task, self).save(*args, **kwargs)
        if need_update:
            from app.tasks import update_task_ctask
            update_task_ctask.delay(self.id)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'Задача #{self.id}'
