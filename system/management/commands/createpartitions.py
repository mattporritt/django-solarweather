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
from django.utils.module_loading import import_string
from django.db import connection
from django.db.models import Max, Min
from psqlextra.partitioning import PostgresPartitioningManager, PostgresPartitioningConfig
from psqlextra.partitioning.range_strategy import PostgresRangePartitioningStrategy



class Command(BaseCommand):
    help = 'Creates table partitions. Will create partitions for all un-partitioned data plus for a month in the future.'

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
        #self.stdout.write(self.style.SUCCESS('Successfully cleared caches'))
        self.stdout.write('Starting partition operations')

        # Loop through the models and get the years that have data.
        for partition_model in Command.partition_models:
            model_obj = import_string(partition_model)
            year_obj = model_obj.objects.values('time_year').distinct()
            for year in year_obj:
                print(year['time_year'])
                # Then get the months that have data.
                month_obj = model_obj.objects.values('time_month').distinct()
                for month in month_obj:
                    print(month['time_month'])
                    # then get the max and min value for each month
                    max_value = model_obj.objects \
                        .filter(time_year=year['time_year'], time_month=month['time_month']) \
                        .aggregate(Max('time_stamp'))
                    min_value = model_obj.objects \
                        .filter(time_year=year['time_year'], time_month=month['time_month']) \
                        .aggregate(Min('time_stamp'))
                    print(max_value)
                    print(min_value)







        # If the month we are processing is the current month get the timestamp for the end of the month for the max

        # Check the partition doesn't already exist.



