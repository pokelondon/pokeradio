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
        make_option('--user',
                    action='store',
                    dest='generate_only',
                    help='Generate only for this screen name'),
        )

    def handle(self, *args, **options):
        if options['generate_only']:
            only = User.objects.get(username=options['generate_only'])
            users = [only,]
        else:
            users = User.objects.all()
        for user in users:
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
