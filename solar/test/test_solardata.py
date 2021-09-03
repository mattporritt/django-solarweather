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
import requests_mock
from solar.solardata import SolarData
from django.conf import settings
import json

import logging

# Get an instance of a logger
logger = logging.getLogger('django')


# Unit testing.
class SolarDataUnitTestCase(TestCase):

    @requests_mock.Mocker()
    def test_get_grid_data(self, m):
        """
        Test getting grid data.
        """

        # Get test data.
        test_json_data = json.dumps(test_data.test_grid_data)

        # Setup mock response.
        inverter_domain = getattr(settings, 'SOLAR_API')
        inverter_uri = 'http://{0}/solar_api/v1/GetMeterRealtimeData.cgi?Scope=System'.format(inverter_domain)
        m.get(inverter_uri, text=test_json_data)

        solar_data = SolarData()
        grid_data = solar_data.get_grid_data()

        self.assertEqual(grid_data['grid_power_usage_real'], 980.11)
        self.assertEqual(grid_data['grid_power_factor'], 0.93)
        self.assertEqual(grid_data['grid_power_apparent'], 1046.23)
        self.assertEqual(grid_data['grid_power_reactive'], -325.19)
        self.assertEqual(grid_data['grid_ac_voltage'], 246)
        self.assertEqual(grid_data['grid_ac_current'], 4.253)

    @requests_mock.Mocker()
    def test_get_inverter_data(self, m):
        """
        Test getting inverter data.
        """

        # Get test data.
        test_json_data = json.dumps(test_data.test_inverter_data)

        # Setup mock response.
        inverter_domain = getattr(settings, 'SOLAR_API')
        inverter_uri = 'http://{0}/solar_api/v1/GetInverterRealtimeData.cgi?Scope=Device&DeviceId=1&DataCollection=CommonInverterData'.format(inverter_domain)
        m.get(inverter_uri, text=test_json_data)

        solar_data = SolarData()
        inverter_data = solar_data.get_inverter_data()

        self.assertEqual(inverter_data['inverter_ac_frequency'], 49.99)
        self.assertEqual(inverter_data['inverter_ac_current'], 0.93)
        self.assertEqual(inverter_data['inverter_ac_voltage'], 242.1)
        self.assertEqual(inverter_data['inverter_ac_power'], 222)
        self.assertEqual(inverter_data['inverter_dc_current'], 0.85)
        self.assertEqual(inverter_data['inverter_dc_voltage'], 309.9)
