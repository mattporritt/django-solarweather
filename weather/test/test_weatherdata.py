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

from django.test import TestCase
from weather.weatherdata import WeatherData
from weather.models import WeatherData as WeatherDataModel
import weather.test.test_data as test_data
from django.core.cache import cache

import logging

# Get an instance of a logger
logger = logging.getLogger('django')


# Basic functional testing
class WeatherDataUnitTestCase(TestCase):
    # Load the fixtures used in this test.
    fixtures = ['weatherdata.json']

    def test_store(self):
        """
        Test storing weather data in the database
        """

        weather_data = WeatherData()
        store_result = weather_data.store(test_data.test_query_vars)

        data_record = WeatherDataModel.objects.get(id=store_result)

        self.assertEqual(data_record.software_type, 'EasyWeatherV1.5.9')

    def test_get_max_day(self):
        """
        Test getting max values from the database for a given day.
        """

        weather_data = WeatherData()
        max_result = weather_data.get_max('solar_radiation', 'day', 1623906568)

        self.assertEqual(max_result.get('solar_radiation__max'), 75.85)

    def test_get_max_month(self):
        """
        Test getting max values from the database for a given month.
        """

        weather_data = WeatherData()
        max_result = weather_data.get_max('solar_radiation', 'month', 1623906568)

        self.assertEqual(max_result.get('solar_radiation__max'), 88.88)

    def test_get_max_year(self):
        """
        Test getting max values from the database for a given year.
        """

        # Start by clearing the cache.
        # If this test was ever run in a production environment it would clear all caches
        cache.clear()

        weather_data = WeatherData()
        max_result = weather_data.get_max('solar_radiation', 'year', 1623906568)

        self.assertEqual(max_result.get('solar_radiation__max'), 90.90)

    def test_get_min_day(self):
        """
        Test getting min values from the database for a given day.
        """

        weather_data = WeatherData()
        min_result = weather_data.get_min('outdoor_temp', 'day', 1623906568)

        self.assertEqual(min_result.get('outdoor_temp__min'), 11.222)

    def test_get_min_month(self):
        """
        Test getting min values from the database for a given month.
        """
        cache.clear()

        weather_data = WeatherData()
        min_result = weather_data.get_min('outdoor_temp', 'month', 1623906568)

        self.assertEqual(min_result.get('outdoor_temp__min'), 10.278)

    def test_get_min_year(self):
        """
        Test getting min values from the database for a given year.
        """

        weather_data = WeatherData()
        min_result = weather_data.get_min('outdoor_temp', 'year', 1623906568)

        self.assertEqual(min_result.get('outdoor_temp__min'), 9.278)

    def test_set_max_year(self):
        """
        Test setting max values to the cache for a given day.
        """

        # Start by clearing the cache.
        # If this test was ever run in a production environment it would clear all caches
        cache.clear()

        cache_key = 'solar_radiation_2021'

        # Initially caches should be empty.
        cache_val = cache.get(cache_key)
        self.assertIsNone(cache_val)

        weather_data = WeatherData()
        max_result = weather_data.set_max('solar_radiation', 'year', 90.91, 1623906568)
        self.assertTrue(max_result)

        # Now check cache contains value.
        cache_val = cache.get(cache_key)
        self.assertEqual(cache_val, 90.91)

    def test_set_max_month(self):
        """
        Test setting max values to the cache for a given day.
        """

        # Start by clearing the cache.
        # If this test was ever run in a production environment it would clear all caches
        cache.clear()

        cache_key = 'solar_radiation_2021_6'
        weather_data = WeatherData()

        # Initially caches should be empty.
        cache_val = cache.get(cache_key)
        self.assertIsNone(cache_val)

        # Initial should be false as less than the current max
        max_result = weather_data.set_max('solar_radiation', 'month', 70.70, 1623906568)
        self.assertFalse(max_result)

        # Month should be updated as greater than stored.
        max_result = weather_data.set_max('solar_radiation', 'month', 89.70, 1623906568)
        self.assertTrue(max_result)

        # But year should not have changed.
        max_result = weather_data.get_max('solar_radiation', 'year', 1623906568)
        self.assertEqual(max_result.get('solar_radiation__max'), 90.90)

        # Update month max to be higher than both year and month max.
        max_result = weather_data.set_max('solar_radiation', 'month', 91.70, 1623906568)
        self.assertTrue(max_result)
        max_result = weather_data.get_max('solar_radiation', 'year', 1623906568)
        self.assertEqual(max_result.get('solar_radiation__max'), 91.70)

        # Now check cache contains value.
        cache_val = cache.get(cache_key)
        self.assertEqual(cache_val, 91.70)

    def test_set_max_day(self):
        """
        Test setting max values to the cache for a given day.
        """

        # Start by clearing the cache.
        # If this test was ever run in a production environment it would clear all caches
        cache.clear()

        cache_key = 'solar_radiation_2021_6_17'
        weather_data = WeatherData()

        # Initially caches should be empty.
        cache_val = cache.get(cache_key)
        self.assertIsNone(cache_val)

        # Initial should be false as less than the current max
        max_result = weather_data.set_max('solar_radiation', 'day', 60.70, 1623906568)
        self.assertFalse(max_result)

        # Day should be updated as greater than stored.
        max_result = weather_data.set_max('solar_radiation', 'day', 75.86, 1623906568)
        self.assertTrue(max_result)

        # But month should not have changed.
        max_result = weather_data.get_max('solar_radiation', 'month', 1623906568)
        self.assertEqual(max_result.get('solar_radiation__max'), 88.88)

        # Update day max to be higher than both month and day max.
        max_result = weather_data.set_max('solar_radiation', 'day', 91.70, 1623906568)
        self.assertTrue(max_result)
        max_result = weather_data.get_max('solar_radiation', 'month', 1623906568)
        self.assertEqual(max_result.get('solar_radiation__max'), 91.70)

        # Now check cache contains value.
        cache_val = cache.get(cache_key)
        self.assertEqual(cache_val, 91.70)

    def test_set_min_year(self):
        """
        Test setting min values to the cache for a given day.
        """

        # Start by clearing the cache.
        # If this test was ever run in a production environment it would clear all caches
        cache.clear()

        cache_key = 'outdoor_temp_2021'

        # Initially caches should be empty.
        cache_val = cache.get(cache_key)
        self.assertIsNone(cache_val)

        weather_data = WeatherData()
        min_result = weather_data.get_min('outdoor_temp', 'year', 1623906568)

        min_result = weather_data.set_min('outdoor_temp', 'year', 8.277, 1623906568)
        self.assertTrue(min_result)

        # Now check cache contains value.
        cache_val = cache.get(cache_key)
        self.assertEqual(cache_val, 8.277)

    def test_set_min_month(self):
        """
        Test setting min values to the cache for a given day.
        """

        # Start by clearing the cache.
        # If this test was ever run in a production environment it would clear all caches
        cache.clear()

        cache_key = 'outdoor_temp_2021_6'
        weather_data = WeatherData()

        # Initially caches should be empty.
        cache_val = cache.get(cache_key)
        self.assertIsNone(cache_val)

        # Initial should be false as greater than the current min
        min_result = weather_data.set_min('outdoor_temp', 'month', 10.279, 1623906568)
        self.assertFalse(min_result)

        # Month should be updated as less than stored.
        min_result = weather_data.set_min('outdoor_temp', 'month', 10.277, 1623906568)
        self.assertTrue(min_result)

        # But year should not have changed.
        min_result = weather_data.get_min('outdoor_temp', 'year', 1623906568)
        self.assertEqual(min_result.get('outdoor_temp__min'), 9.278)

        # Update month min to be lower than both year and month min.
        min_result = weather_data.set_min('outdoor_temp', 'month', 9.277, 1623906568)
        self.assertTrue(min_result)
        min_result = weather_data.get_min('outdoor_temp', 'year', 1623906568)
        self.assertEqual(min_result.get('outdoor_temp__min'), 9.277)

        # Now check cache contains value.
        cache_val = cache.get(cache_key)
        self.assertEqual(cache_val, 9.277)

    def test_set_min_day(self):
        """
        Test setting min values to the cache for a given day.
        """

        # Start by clearing the cache.
        # If this test was ever run in a production environment it would clear all caches
        cache.clear()

        cache_key = 'outdoor_temp_2021_6_17'
        weather_data = WeatherData()

        # Initially caches should be empty.
        cache_val = cache.get(cache_key)
        self.assertIsNone(cache_val)

        # Initial should be false as less than the current min
        min_result = weather_data.set_min('outdoor_temp', 'day', 11.222, 1623906568)
        self.assertFalse(min_result)

        # Day should be updated as less than stored.
        min_result = weather_data.set_min('outdoor_temp', 'day', 11.221, 1623906568)
        self.assertTrue(min_result)

        # But month should not have changed.
        min_result = weather_data.get_min('outdoor_temp', 'month', 1623906568)
        self.assertEqual(min_result.get('outdoor_temp__min'), 10.278)

        # Update day min to be lower than both month and day min.
        min_result = weather_data.set_min('outdoor_temp', 'day', 10.277, 1623906568)
        self.assertTrue(min_result)
        min_result = weather_data.get_min('outdoor_temp', 'month', 1623906568)
        self.assertEqual(min_result.get('outdoor_temp__min'), 10.277)

        # Now check cache contains value.
        cache_val = cache.get(cache_key)
        self.assertEqual(cache_val, 10.277)
