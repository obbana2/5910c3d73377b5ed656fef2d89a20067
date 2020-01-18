import random
import string
import requests
from django.utils import timezone
from django.conf import settings

from app.models import Task


def request_points(func, dt, interval):
    response = requests.post('http://service2:5001/api/actions/gendata', json={
        'func': func,
        'dt': dt,
        'interval': interval,
    })
    return response.json()


def request_chart(data):
    response = requests.post('http://service3:5002/api/actions/genchart', json={
        'data': data,
    })
    if response.status_code == 200:
        filename = '/img/{}.png'.format(''.join(random.choices(string.ascii_lowercase + string.digits, k=10)))
        with open(settings.MEDIA_ROOT + filename, 'wb') as f:
            f.write(response.content)
        return {
            'service': 'service3',
            'status': 'success',
            'result': filename,
        }
    else:
        return response.json()


def update_task(id):
    task = None
    try:
        task = Task.objects.get(pk=id)

        response = request_points(task.get_func_display(), task.dt, task.interval)
        if response['status'] == 'error':
            return response

        response = request_chart(response['result'])
        if response['status'] == 'error':
            return response

        result = {
            'service': 'service1',
            'status': 'success',
            'result': response['result'],
        }
    except Exception as e:
        result = {
            'service': 'service1',
            'status': 'error',
            'message': str(e),
        }

    if task:
        if result['status'] == 'error':
            task.result = 'Ошибка {}: {}'.format(result['service'], result['message'])
        else:
            task.result = result['result']
        task.date = timezone.now()
        task.save()

    return result
