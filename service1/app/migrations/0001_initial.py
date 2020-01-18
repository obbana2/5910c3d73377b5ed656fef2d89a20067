# Generated by Django 3.0.2 on 2020-01-16 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('func', models.PositiveIntegerField(choices=[(1, 't + 2/t'), (2, 'sin(t)')], verbose_name='Функция')),
                ('result', models.CharField(max_length=255, verbose_name='График')),
                ('interval', models.PositiveIntegerField(verbose_name='Интервал')),
                ('date', models.DateTimeField(null=True, verbose_name='Дата обработки')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
    ]
