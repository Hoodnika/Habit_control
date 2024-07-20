from django.core.management import BaseCommand

from userapp.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            tg_username='admin',
            first_name='Admin',
            last_name='Admin',
            is_superuser=True,
            is_staff=True
        )
        user.set_password('57365')
        user.save()
