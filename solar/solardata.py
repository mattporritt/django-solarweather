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

import requests
from django.conf import settings
import logging

# Get an instance of a logger
logger = logging.getLogger('django')

class SolarData:
    """
    Class to get inverter data and related operations.
    """

    @staticmethod
    def get_grid_data() -> dict:
        """

        :return:
        """

        inverter_domain = getattr(settings, 'SOLAR_API')
        inverter_uri = 'http://{0}/solar_api/v1/GetMeterRealtimeData.cgi'.format(inverter_domain)
        query_params = {'Scope': 'System'}
        request_response = requests.get(inverter_uri, params=query_params)
        grid_data_raw = request_response.json()['Body']['Data']['0']

        # Just grab the data we want.
        grid_data = {
            'grid_power_usage_real': grid_data_raw.get('PowerReal_P_Sum', 0),
            'grid_power_factor': grid_data_raw.get('PowerFactor_Sum', 0),
            'grid_power_apparent': grid_data_raw.get('PowerApparent_S_Sum', 0),
            'grid_power_reactive': grid_data_raw.get('PowerReactive_Q_Sum', 0),
            'grid_ac_voltage': grid_data_raw.get('Voltage_AC_Phase_1', 0),
            'grid_ac_current': grid_data_raw.get('Current_AC_Sum', 0)
        }

        return grid_data

    @staticmethod
    def get_inverter_data() -> dict:
        """

        :return:
        """

        inverter_domain = getattr(settings, 'SOLAR_API')
        inverter_uri = 'http://{0}/solar_api/v1/GetInverterRealtimeData.cgi'.format(inverter_domain)
        query_params = {'Scope': 'Device', 'DeviceId': '1', 'DataCollection': 'CommonInverterData'}
        request_response = requests.get(inverter_uri, params=query_params)
        inverter_data_raw = request_response.json()['Body']['Data']

        # Just grab the data we want.
        inverter_data = {
            'inverter_ac_frequency': inverter_data_raw.get('FAC', {'Unit': 'Hz', 'Value': 0})['Value'],
            'inverter_ac_current': inverter_data_raw.get('IAC', {'Unit': 'A', 'Value': 0})['Value'],
            'inverter_ac_voltage': inverter_data_raw.get('UAC', {'Unit': 'V', 'Value': 0})['Value'],
            'inverter_ac_power': inverter_data_raw.get('PAC', {'Unit': 'W', 'Value': 0})['Value'],
            'inverter_dc_current': inverter_data_raw.get('IDC', {'Unit': 'A', 'Value': 0})['Value'],
            'inverter_dc_voltage': inverter_data_raw.get('UDC', {'Unit': 'V', 'Value': 0})['Value']
        }

        return inverter_data
