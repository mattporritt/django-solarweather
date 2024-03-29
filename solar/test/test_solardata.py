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
from solar.models import SolarData as SolarDataModel
from django.core.cache import cache
from datetime import datetime

import logging

# Get an instance of a logger
logger = logging.getLogger('django')


# Unit testing.
class SolarDataUnitTestCase(TestCase):
    # Load the fixtures used in this test.
    fixtures = ['solardata.json']

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

    @requests_mock.Mocker()
    def test_get_inverter_data_dark(self, m):
        """
        Test getting inverter data when it is dark outside.
        When the inverter is not generating any power,
        the response object has a different signature.
        """

        # Get test data.
        test_json_data = json.dumps(test_data.test_inverter_data_dark)

        # Setup mock response.
        inverter_domain = getattr(settings, 'SOLAR_API')
        inverter_uri = 'http://{0}/solar_api/v1/GetInverterRealtimeData.cgi?Scope=Device&DeviceId=1&DataCollection=CommonInverterData'.format(inverter_domain)
        m.get(inverter_uri, text=test_json_data)

        solar_data = SolarData()
        inverter_data = solar_data.get_inverter_data()

        self.assertEqual(inverter_data['inverter_ac_frequency'], 0)
        self.assertEqual(inverter_data['inverter_ac_current'], 0)
        self.assertEqual(inverter_data['inverter_ac_voltage'], 0)
        self.assertEqual(inverter_data['inverter_ac_power'], 0)
        self.assertEqual(inverter_data['inverter_dc_current'], 0)
        self.assertEqual(inverter_data['inverter_dc_voltage'], 0)

    @requests_mock.Mocker()
    def test_store(self, m):
        """
        Test getting inverter data.
        """

        # Get test data.
        grid_test_json_data = json.dumps(test_data.test_grid_data)
        inverter_test_json_data = json.dumps(test_data.test_inverter_data)

        # Setup mock response.
        inverter_domain = getattr(settings, 'SOLAR_API')
        inverter_uri = 'http://{0}/solar_api/v1/GetMeterRealtimeData.cgi?Scope=System'.format(inverter_domain)
        m.get(inverter_uri, text=grid_test_json_data)

        inverter_uri = 'http://{0}/solar_api/v1/GetInverterRealtimeData.cgi?Scope=Device&DeviceId=1&DataCollection=CommonInverterData'.format(inverter_domain)
        m.get(inverter_uri, text=inverter_test_json_data)

        solar_data = SolarData()
        store_result = solar_data.store()
        store_result['thread'].join()

        data_record = SolarDataModel.objects.get(id=store_result['datarecord'])

        self.assertEqual(data_record.inverter_ac_frequency, 49.99)

    def test_set_latest(self):
        """
        Test setting the latest value.
        """

        # Start by clearing the cache.
        # If this test was ever run in a production environment it would clear all caches
        cache.clear()

        cache_key = 'inverter_ac_voltage_latest'
        solar_data = SolarData()

        # Initially caches should be empty.
        cache_val = cache.get(cache_key)
        self.assertIsNone(cache_val)

        # Initial should be false as less than the current min
        set_result = solar_data.set_latest('inverter_ac_voltage', 10.277)
        self.assertEqual(set_result.get('inverter_ac_voltage_latest'), 10.277)

    def test_get_latest(self):
        """
        Test getting the latest value.
        """

        # Start by clearing the cache.
        # If this test was ever run in a production environment it would clear all caches
        cache.clear()

        cache_key = 'inverter_ac_voltage_latest'
        solar_data = SolarData()

        # Initially caches should be empty.
        cache_val = cache.get(cache_key)
        self.assertIsNone(cache_val)

        cache.set(cache_key, 10.277)

        # Initial should be false as less than the current min
        set_result = solar_data.get_latest('inverter_ac_voltage')
        self.assertEqual(set_result.get('inverter_ac_voltage_latest'), 10.277)

    def test_get_date_obj(self):
        """
        Test the date object processing.
        """

        timestamp = 1632429492

        solar_data = SolarData()
        date_obj = solar_data.get_date_obj(timestamp)

        self.assertEqual(date_obj['year'], 2021)
        self.assertEqual(date_obj['month'], 9)
        self.assertEqual(date_obj['week'], 38)
        self.assertEqual(date_obj['day'], 24)
        self.assertEqual(date_obj['week_start_day'], 19)
        self.assertEqual(date_obj['week_end_day'], 25)

    def test_get_accumulated_area(self):
        """
        Test getting the accumulated data.
        """

        data_set = [
            {'time_stamp': 1631858701, 'inverter_ac_power': 1308.0},
            {'time_stamp': 1631858721, 'inverter_ac_power': 1323.0},
            {'time_stamp': 1631858741, 'inverter_ac_power': 1653.0},
            {'time_stamp': 1631858761, 'inverter_ac_power': 2249.0},
            {'time_stamp': 1631858781, 'inverter_ac_power': 1968.0},
            {'time_stamp': 1631858801, 'inverter_ac_power': 1263.0},
            {'time_stamp': 1631858821, 'inverter_ac_power': 1206.0},
            {'time_stamp': 1631858841, 'inverter_ac_power': 1173.0},
            {'time_stamp': 1631858861, 'inverter_ac_power': 1155.0},
            {'time_stamp': 1631858882, 'inverter_ac_power': 1155.0},
            {'time_stamp': 1631858902, 'inverter_ac_power': 1167.0},
        ]

        solar_data = SolarData()

        # Test.
        accum_area = solar_data.get_accumulated_area(data_set, 'inverter_ac_power', 'time_stamp')
        self.assertEqual(accum_area, 79.44027777777778)

    def test_get_accumulated(self):
        """
        Test getting accumulated data.
        """
        # Start by clearing the cache.
        # If this test was ever run in a production environment it would clear all caches
        cache.clear()

        metric = 'inverter_ac_power'
        time_obj = {
            'year': 2021,
            'month': 10,
            'week': 38,
            'day': 17,
            'week_start_day': 17,
            'week_end_day': 23,
        }

        solar_data = SolarData()

        # Test year.
        accum_val = solar_data.get_accumulated(metric, 'year', time_obj)
        self.assertEqual(accum_val, 4020.651527777777)

        # Test month.
        accum_val = solar_data.get_accumulated(metric, 'month', time_obj)
        self.assertEqual(accum_val, 19.875)

        # Test week.
        accum_val = solar_data.get_accumulated(metric, 'week', time_obj)
        self.assertEqual(accum_val, 19.875)

        # Test day.
        accum_val = solar_data.get_accumulated(metric, 'day', time_obj)
        self.assertEqual(accum_val, 14.258333333333335)

    def test_get_trend(self):
        """
        Test getting the trend data.
        """

        # Start by clearing the cache.
        # If this test was ever run in a production environment it would clear all caches.
        cache.clear()

        date_object = datetime.fromtimestamp(1631859241)
        time_obj = {
            'year': date_object.year,
            'month': date_object.month,
            'day': date_object.day
        }

        solar_data = SolarData()
        result_data = solar_data.get_trend('grid_power_usage_real', 'day', time_obj)

        self.assertEqual(result_data[0][0], 1631855161)
        self.assertEqual(result_data[-1][0], 1631859241)

    def test_get_date_range(self):
        """
        Test getting the date range.
        """

        # Start by clearing the cache.
        # If this test was ever run in a production environment it would clear all caches.
        cache.clear()

        today = datetime.now().strftime("%Y-%m-%d")

        solar_data = SolarData()
        result_data = solar_data.get_date_range()

        self.assertEqual(result_data['value'], today)
        self.assertEqual(result_data['maximum'], '2022-10-18')
        self.assertEqual(result_data['minimum'], '2021-09-17')
