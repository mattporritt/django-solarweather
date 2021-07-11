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

import logging

# Get an instance of a logger
logger = logging.getLogger('django')


# Basic functional testing
class WeatherDataUnitTestCase(TestCase):
    fixtures = ['weatherdata.json']

    def test_store(self):
        """
        Test storing weather data in the database
        """

        weather_data = WeatherData()
        store_result = weather_data.store(test_data.test_query_vars)

        data_record = WeatherDataModel.objects.get(id=store_result)

        self.assertEqual(data_record.software_type, 'EasyWeatherV1.5.9')

    def test_get_max(self):
        """
        Test getting max values from the database.
        """

        weather_data = WeatherData()
        max_result = weather_data.get_max('solar_radiation', 'day', 1623906568)

        logger.info(max_result)
