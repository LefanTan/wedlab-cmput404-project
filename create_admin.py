from django.contrib.auth.models import User

User.objects.create_superuser(username='team02admin', password='admin')
