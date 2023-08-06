from django.core.management import call_command
from django.core.management.base import BaseCommand

from ...signals import periodic_task


class Command(BaseCommand):
    help = "Rebuild static files and language files"

    def handle(self, *args, **options):
        periodic_task.send(self)
        call_command('compilemessages', verbosity=1, interactive=False)
        call_command('compilejsi18n', verbosity=1, interactive=False)
        call_command('collectstatic', verbosity=1, interactive=False)
        call_command('compress', verbosity=1, interactive=False)
