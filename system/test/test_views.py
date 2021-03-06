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

from django.test import TestCase, Client
from django.core.cache import cache
import json

import logging

# Get an instance of a logger
logger = logging.getLogger('django')


# Basic functional testing
class SystemFunctionalTestCase(TestCase):
    # Load the fixtures used in this test.
    fixtures = ['weatherdata.json']

    def setUp(self):
        self.client = Client()

    def test_dataajax_weather_view(self):
        cache.clear()
        response = self.client.get('/dataajax/?dashboard=weather', {'timestamp': '1623906568'})
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['indoor_temp']['daily_min'], 19.722)
        self.assertEqual(content['indoor_temp']['daily_max'], 20.0)
        self.assertEqual(content['indoor_temp']['daily_trend'][0][0], 1623906326)
        self.assertEqual(content['indoor_temp']['daily_trend'][-1][0], 1623907827)
