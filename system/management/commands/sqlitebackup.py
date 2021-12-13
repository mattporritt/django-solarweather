# ==============================================================================
#
# This file is part of SolarWeather.
#
# SolarWeather is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SolarWeather is distributed  WITHOUT ANY WARRANTY:
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.
# ==============================================================================

# ==============================================================================
#
# @author Matthew Porritt
# @copyright  2021 onwards Matthew Porritt (mattp@catalyst-au.net)
# @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
# ==============================================================================

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import sqlite3
import time


class Command(BaseCommand):
    help = 'Export the SQLite Database'

    def add_arguments(self, parser):
        """
        Arguments for the command.
        """
        parser.add_argument(
            'path',
            type=str,
            help='The path to save the backup file. e.g /tmp/db.sql'
        )

    def handle(self, *args, **options):
        """
        Export the SQLite database.
        """
        db_settings = inverter_domain = getattr(settings, 'DATABASES')
        db_con = sqlite3.connect(db_settings['default']['NAME'])
        start = time.time()
        path = options['path']

        self.stdout.write(self.style.SUCCESS('Beginning database backup.'))
        with open(path, 'w') as f:
            for line in db_con.iterdump():
                f.write('%s\n' % line)
        db_con.close()

        total_time = (time.time() - start)
        self.stdout.write(self.style.SUCCESS('Backup complete in {0:.1f} seconds.'.format(total_time)))
