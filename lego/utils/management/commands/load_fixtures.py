import logging
import os
from datetime import timedelta

from django.conf import settings
from django.core.management import call_command
from django.utils import timezone

from lego.apps.events.models import Event
from lego.apps.files.storage import storage
from lego.apps.social_groups.fixtures.development_interest_groups import load_dev_interest_groups
from lego.apps.users.fixtures.initial_abakus_groups import load_abakus_groups
from lego.apps.users.fixtures.test_abakus_groups import load_test_abakus_groups
from lego.utils.management_command import BaseCommand

log = logging.getLogger(__name__)


class Command(BaseCommand):

    help = 'Loads initial data from fixtures.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--development',
            action='store_true',
            default=False,
            help='Load development fixtures.',
        )
        parser.add_argument(
            '--generate',
            action='store_true',
            default=False,
            help='Generate fixtures',
        )

    def run(self, *args, **options):
        log.info('Loading regular fixtures:')

        # Helpers
        uploads_bucket = getattr(settings, 'AWS_S3_BUCKET', None)

        def upload_file(file, key):
            """
            Helper function for file uploads to S3
            """
            assets_folder = os.path.join(settings.BASE_DIR, '../assets')
            local_file = os.path.join(assets_folder, file)
            log.info(f'Uploading {key} file to bucket')
            storage.upload_file(uploads_bucket, key, local_file)

        if options['generate']:
            self.generate_groups()

        call_command('loaddata', 'lego/apps/files/fixtures/initial_files.yaml')
        call_command('loaddata', 'lego/apps/users/fixtures/initial_abakus_groups.yaml')
        call_command('loaddata', 'lego/apps/users/fixtures/initial_users.yaml')
        call_command('loaddata', 'lego/apps/users/fixtures/initial_memberships.yaml')
        call_command('loaddata', 'lego/apps/tags/fixtures/initial_tags.yaml')

        if getattr(settings, 'DEVELOPMENT', None) or options['development']:
            log.info('Loading development fixtures:')
            call_command('loaddata', 'lego/apps/users/fixtures/development_users.yaml')
            call_command('loaddata', 'lego/apps/files/fixtures/development_files.yaml')

            # Prepare storage bucket for development. We skips this in production.
            # The bucket needs to be created manually.
            log.info(f'Makes sure the {uploads_bucket} bucket exists')
            storage.create_bucket(uploads_bucket)
            upload_file('abakus.png', 'abakus.png')
            upload_file('test_event_cover.png', 'test_event_cover.png')
            upload_file('test_article_cover.png', 'test_article_cover.png')
            upload_file('default_male_avatar.png', 'default_male_avatar.png')
            upload_file('default_male_avatar.png', 'default_other_avatar.png')
            upload_file('default_female_avatar.png', 'default_female_avatar.png')
            upload_file('abakus_logo.png', 'abakus_logo.png')
            upload_file('abakus_bedkom.png', 'abakus_bedkom.png')
            upload_file('abakus_koskom.png', 'abakus_koskom.png')
            upload_file('abakus_labamba.png', 'abakus_labamba.png')
            upload_file('abakus_readme.png', 'abakus_readme.png')
            upload_file('abakus_webkom.png', 'abakus_webkom.png')

            call_command(
                'loaddata',
                'lego/apps/social_groups/fixtures/development_interest_groups.yaml'
            )
            call_command('loaddata', 'lego/apps/gallery/fixtures/development_galleries.yaml')
            call_command('loaddata', 'lego/apps/users/fixtures/development_memberships.yaml')
            call_command('loaddata', 'lego/apps/companies/fixtures/development_companies.yaml')
            call_command('loaddata', 'lego/apps/events/fixtures/development_events.yaml')
            call_command('loaddata', 'lego/apps/events/fixtures/development_pools.yaml')
            call_command('loaddata', 'lego/apps/events/fixtures/development_registrations.yaml')
            call_command('loaddata', 'lego/apps/flatpages/fixtures/development_pages.yaml')
            call_command('loaddata', 'lego/apps/articles/fixtures/development_articles.yaml')
            call_command('loaddata', 'lego/apps/quotes/fixtures/development_quotes.yaml')
            call_command('loaddata', 'lego/apps/oauth/fixtures/development_applications.yaml')
            call_command('loaddata', 'lego/apps/reactions/fixtures/emojione_reaction_types.yaml')
            call_command('loaddata', 'lego/apps/joblistings/fixtures/development_joblistings.yaml')
            self.update_event_dates()
        log.info('Done!')

    @staticmethod
    def update_event_dates():
        date = timezone.now().replace(hour=16, minute=15, second=0, microsecond=0)
        for i, event in enumerate(Event.objects.all()):
            event.start_time = date + timedelta(days=i-10)
            event.end_time = date + timedelta(days=i-10, hours=4)
            event.save()
            for j, pool in enumerate(event.pools.all()):
                pool.activation_date = date.replace(hour=12, minute=0) + timedelta(days=i-j-16)
                pool.save()

    @staticmethod
    def generate_groups():
        call_command('flush', '--noinput')  # Need to reset the pk counter to start pk on 1
        call_command('migrate')
        load_abakus_groups()
        with open('lego/apps/users/fixtures/initial_abakus_groups.yaml', 'w') as f:
            f.write("#\n# THIS FILE IS HANDLED BY `load_fixtures`"
                    " and `initial_abakus_groups.py`\n#\n")
            call_command('dumpdata', '--format=yaml', 'users.AbakusGroup', stdout=f)

        load_dev_interest_groups()

        with open('lego/apps/social_groups/fixtures/development_interest_groups.yaml', 'w') as f:
            f.write("#\n# THIS FILE IS HANDLED BY `load_fixtures`"
                    " and `development_interest_groups.py`\n#\n")
            call_command('dumpdata', '--format=yaml', 'users.AbakusGroup', stdout=f)
            call_command('dumpdata', '--format=yaml', 'social_groups.InterestGroup', stdout=f)

        load_test_abakus_groups()

        with open('lego/apps/users/fixtures/test_abakus_groups.yaml', 'w') as f:
            f.write("#\n# THIS FILE IS HANDLED BY `load_fixtures`"
                    " and `development_interest_groups.py`\n#\n")
            call_command('dumpdata', '--format=yaml', 'users.AbakusGroup', stdout=f)
