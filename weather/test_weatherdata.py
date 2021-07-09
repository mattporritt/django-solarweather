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


# Basic functional testing
class WeatherDataUnitTestCase(TestCase):

    def test_store(self):
        
        # Sample of test data that is sent from the weather station.
        request_data = {
            'ID' : 'IVCTMERN2',
            'PASSWORD': 'reflhd33',
            'indoortempf': '68.0',
            'tempf': '52.5',
            'dewptf': '45.5',
            'windchillf': '52.5',
            'indoorhumidity': '52',
            'humidity': '77',
            'windspeedmph': '0.7',
            'windgustmph': '1.1',
            'winddir': '338',
            'absbaromin': '29.318',
            'baromin': '29.714',
            'rainin': '0.000',
            'dailyrainin': '0.000',
            'weeklyrainin': '0.181',
            'monthlyrainin': '3.098',
            'solarradiation': '71.56',
            'UV': '0',
            'dateutc': '2021-06-17%2005:08:28',
            'softwaretype': 'EasyWeatherV1.5.9',
            'action': 'updateraw',
            'realtime': '1',
            'rtfreq': '5',
            }

        weather_data = WeatherData()
        store_result = weather_data.store(request_data)

        self.assertEqual(store_result, 0)
