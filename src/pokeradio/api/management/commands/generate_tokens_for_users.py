import uuid

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from pokeradio.api.models import Token

class Command(BaseCommand):
    help = 'Generate API tokens for users who don\'t currently have one'
    option_list = BaseCommand.option_list + (
        make_option('--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Report token operations without carrying them out'),
        )

    def handle(self, *args, **options):
        for user in User.objects.all():
            self.stdout.write('%s... ' % user)
            if user.tokens.filter(enabled=True).count() == 0:
                if options['dry_run']:
                    self.stdout.write('no enabled token')
                else:
                    self.stdout.write('no enabled token, creating... ')
                    t = Token()
                    t.user = user
                    t.token = str(uuid.uuid4())
                    t.save()
                    self.stdout.write('done\n')
            else:
                self.stdout.write('token exists\n')
