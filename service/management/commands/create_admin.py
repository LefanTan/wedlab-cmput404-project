from this import d
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create super user"

    def handle(self, *args, **options):
        try:
            User.objects.get(username='team02admin')
            print('Super admin already made')
        except:
            User.objects.create_superuser(
                username='team02admin', password='admin')
            print("Super admin created!")
