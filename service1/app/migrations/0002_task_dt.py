# Generated by Django 3.0.2 on 2020-01-16 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='dt',
            field=models.PositiveIntegerField(default=0, verbose_name='Шаг в часах'),
            preserve_default=False,
        ),
    ]