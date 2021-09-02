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
import solar.test.test_data as test_data
import responses
from solar.solardata import SolarData
from django.conf import settings
import json

import logging

# Get an instance of a logger
logger = logging.getLogger('django')


# Unit testing.
class SolarDataUnitTestCase(TestCase):

    def test_get_grid_data(self):
        """
        Test getting grid data.
        """

        # Get test data.
        test_json_data = json.dumps(test_data.test_grid_data)

        # Setup mock response.
        inverter_domain = getattr(settings, 'SOLAR_API')
        inverter_uri = 'http://{0}/solar_api/v1/GetMeterRealtimeData.cgi'.format(inverter_domain)
        responses.add(responses.GET, inverter_uri, json=test_json_data, status=200)

        solar_data = SolarData()
        grid_data = solar_data.get_grid_data()

        logger.info(grid_data)


