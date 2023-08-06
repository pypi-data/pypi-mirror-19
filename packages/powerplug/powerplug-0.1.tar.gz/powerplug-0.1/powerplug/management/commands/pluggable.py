

from pkg_resources import working_set

import powerplug
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('subcommand')

    def handle(self, *args, **options):
        if options['subcommand'] == 'list':
            return self._list(*args, **options)

    def _list(self, *args, **options):
        print('Installed Apps')
        for entry in working_set.iter_entry_points(powerplug.ENTRY_POINT_APP):
            print('\t', entry.module_name)
        print('Installed APIs')
        for entry in working_set.iter_entry_points(powerplug.ENTRY_POINT_API):
            print('\t', entry.module_name)
