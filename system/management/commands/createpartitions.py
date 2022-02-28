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

from django.core.management.base import BaseCommand
from django.utils.module_loading import import_string
from django.db import connection
from django.db.models import Max, Min
from datetime import datetime
from dateutil import relativedelta
import calendar

import logging
logger = logging.getLogger('django')

class Command(BaseCommand):
    help = 'Creates table partitions. Will create partitions for all un-partitioned data plus a month in the future.'

    # Models to create partitions for.
    partition_models = [
        'solar.models.SolarData',
        'weather.models.WeatherData',
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry",
            "-d",
            action="store_true",
            help="When specified, no partitions will be created. Just a simulation.",
            required=False,
            default=False,
        )

    def handle(self, dry: bool, *args, **kwargs):
        self.stdout.write('Gathering data on partitions to create...')

        partition_list = []
        current_month = datetime.now().month
        current_year = datetime.now().year
        next_month_obj = datetime.today() + relativedelta.relativedelta(months=1)
        next_month = next_month_obj.month
        next_year = next_month_obj.year
        next_month_str = str(next_month).zfill(2)
        next_year_str = str(next_year).zfill(2)

        # Loop through the models and get the years that have data.
        for partition_model in Command.partition_models:
            model_obj = import_string(partition_model)
            app_model_name = partition_model.split('.')
            app_name = app_model_name[0].lower()
            model_name = app_model_name[2].lower()

            year_obj = model_obj.objects.values('time_year').distinct()

            for year in year_obj:
                # Then get the months that have data.
                month_obj = model_obj.objects.values('time_month').distinct()
                for month in month_obj:
                    # If table exists, exit early.
                    table_name = '{}_{}_{}_{}'.format(app_name, model_name, year['time_year'], month['time_month'])
                    if table_name in connection.introspection.table_names():
                        return

                    # Then get the max and min value for each month.
                    min_value = model_obj.objects \
                        .filter(time_year=year['time_year'], time_month=month['time_month']) \
                        .aggregate(Min('time_stamp'))

                    # If the month we are processing is the current month,
                    # get the timestamp for the end of the month for the max.
                    if (year['time_year'] == current_year) and (month['time_month'] == current_month):
                        month_range = calendar.monthrange(year['time_year'], month['time_month'])
                        max_value = {
                            'time_stamp__max': int(datetime(
                                year['time_year'],
                                month['time_month'],
                                month_range[1],
                                23, 59, 59).timestamp())
                        }
                    else:
                        max_value = model_obj.objects \
                            .filter(time_year=year['time_year'], time_month=month['time_month']) \
                            .aggregate(Max('time_stamp'))

                    if (max_value['time_stamp__max'] is not None) and (min_value['time_stamp__min'] is not None):
                        partition_dict = {
                            'model': model_obj,
                            'name': '{}_{}'.format(year['time_year'], month['time_month']),
                            'from_values': min_value['time_stamp__min'],
                            'to_values': max_value['time_stamp__max']
                        }
                        partition_list.append(partition_dict)

            # Create partition for next month.
            # Only create if table doesn't exist.
            table_name = '{}_{}_{}_{}'.format(app_name, model_name, next_year_str, next_month_str)
            logger.info(table_name)
            if table_name not in connection.introspection.table_names():
                month_range = calendar.monthrange(next_year, next_month)
                max_value = int(datetime(
                        next_year,
                        next_month,
                        month_range[1],
                        23, 59, 59).timestamp())
                min_value = int(datetime(
                    next_year,
                    next_month,
                    1,
                    0, 0, 0).timestamp())

                partition_dict = {
                    'model': model_obj,
                    'name': '{}_{}'.format(next_year_str, next_month_str),
                    'from_values': min_value,
                    'to_values': max_value
                }
                partition_list.append(partition_dict)

        # Exit early if dry run.
        if dry:
            return

        self.stdout.write('Creating partitions')
        for partition in partition_list:
            connection.schema_editor().add_range_partition(**partition)
