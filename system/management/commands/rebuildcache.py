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
from django.core.cache import cache
from weather.weatherdata import WeatherData
from solar.solardata import SolarData
from datetime import datetime
import time


class Command(BaseCommand):
    help = 'Clears the application cache'

    def handle(self, *args, **options):
        timestamp = datetime.now().timestamp()
        date_object = datetime.fromtimestamp(timestamp)
        time_obj = {
            'year': date_object.year,
            'month': date_object.month,
            'day': date_object.day
        }

        # Clear caches.
        cache.clear()
        self.stdout.write(self.style.SUCCESS('Successfully cleared caches.'))

        # Rebuild caches.
        start = time.time()
        self.stdout.write(self.style.SUCCESS('Rebuilding caches.'))

        self.stdout.write(self.style.SUCCESS('Getting Weather data...'))
        weather_start_time = time.time()
        weather_data = WeatherData.get_data()
        self.stdout.write(self.style.SUCCESS('Weather data fetched: {0:.1f} seconds'.format(time.time() - weather_start_time)))

        self.stdout.write(self.style.SUCCESS('Setting Weather data cache...'))
        for metric, value in weather_data.items():
            WeatherData.set_max(metric, 'day', value['daily_max'], time_obj)
            WeatherData.set_max(metric, 'month', value['monthly_min'], time_obj)
            WeatherData.set_max(metric, 'year', value['yearly_max'], time_obj)

            WeatherData.set_min(metric, 'day', value['daily_max'], time_obj)
            WeatherData.set_min(metric, 'month', value['monthly_min'], time_obj)
            WeatherData.set_min(metric, 'year', value['yearly_min'], time_obj)

            WeatherData.set_latest(metric, value['latest'])
        self.stdout.write(self.style.SUCCESS('Weather cache set.'))

        self.stdout.write(self.style.SUCCESS('Getting Solar data...'))
        solar_start_time = time.time()
        solar_data = SolarData.get_data()
        self.stdout.write(self.style.SUCCESS('Solar data fetched: {0:.1f} seconds'.format(time.time() - solar_start_time)))

        self.stdout.write(self.style.SUCCESS('Setting Solar data cache...'))
        for metric, value in solar_data.items():
            if metric == 'solar_radiation' or metric == 'uv_index':
                continue
            SolarData.get_accumulated(metric, 'day', time_obj, False)
            SolarData.get_accumulated(metric, 'month', time_obj, False)
            SolarData.get_accumulated(metric, 'year',time_obj, False)

            SolarData.set_latest(metric, value['latest'])
        self.stdout.write(self.style.SUCCESS('Solar cache set.'))

        # Test cache values.
        self.stdout.write(self.style.SUCCESS('Getting cached Weather data...'))
        weather_start_time = time.time()
        WeatherData.get_data()
        self.stdout.write(self.style.SUCCESS('Weather data fetched: {0:.1f} seconds'.format(time.time() - weather_start_time)))

        self.stdout.write(self.style.SUCCESS('Getting cached Solar data...'))
        solar_start_time = time.time()
        SolarData.get_data()
        self.stdout.write(self.style.SUCCESS('Solar data fetched: {0:.1f} seconds'.format(time.time() - solar_start_time)))
