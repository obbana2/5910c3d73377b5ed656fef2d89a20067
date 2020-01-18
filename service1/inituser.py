import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service1.settings")
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if User.objects.all().count() == 0:
    User.objects.create_superuser('admin', 'admin@example.com', '11122211')
