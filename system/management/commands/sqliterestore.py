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
import os
import tqdm


class Command(BaseCommand):
    help = 'Import SQLite Database from backup'

    def add_arguments(self, parser):
        """
        Arguments for the command.
        """
        parser.add_argument(
            'path',
            type=str,
            help='The path to the backup file to restore. e.g /tmp/db.sql'
        )

    def handle(self, *args, **options):
        """
        Import the SQLite database.
        """
        db_settings = getattr(settings, 'DATABASES')
        db_name = db_settings['default']['NAME']
        start = time.time()
        path = options['path']

        # Check backup file exists.
        if not os.path.isfile(path):
            self.stdout.write(self.style.ERROR('Database backup file does not exist'))
            exit(1)

        # Delete database if it exists.
        if os.path.isfile(db_name):
            self.stdout.write(self.style.WARNING('Database exists, removing'))
            os.remove(db_name)
        else:
            self.stdout.write(self.style.WARNING('Database does not exist, creating {}'.format(db_name)))

        # Create database.
        db_con = sqlite3.connect(db_name)
        db_cur = db_con.cursor()

        # Restore database from file.
        self.stdout.write(self.style.SUCCESS('Starting database restore...'))
        with tqdm.tqdm(total=os.path.getsize(path)) as pbar:
            with open(path) as file:
                for line in file:
                    db_cur.execute(line)
                    pbar.update(len(line))

        # Test database.
        db_cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.stdout.write(self.style.SUCCESS('Tables created:'))
        for row in db_cur.fetchall():
            db_cur.execute("SELECT COUNT(*) FROM '{}';".format(row[0]))
            self.stdout.write(self.style.SUCCESS('Table {}, Rows {}'.format(row[0], db_cur.fetchone()[0])))
        db_con.close()

        total_time = (time.time() - start)
        self.stdout.write(self.style.SUCCESS('Restore complete in {0:.1f} seconds.'.format(total_time)))
