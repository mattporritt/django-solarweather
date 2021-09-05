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
from datetime import datetime
from solar.models import SolarData as SolarDataModel


class SolarData:
    """
    Class to get inverter data and related operations.
    """

    @staticmethod
    def get_grid_data() -> dict:
        """
        Query the Fronius inverter for grid power data.

        :return grid_data: The grid data received from the inverter.
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
        Query the Fronius inverter for inverter and solar power data.

        :return inverter_data: The solar data received from the inverter.
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


    @staticmethod
    def store(timestamp: int = 0) -> int:
        """
        Store received weather station data into database.

        :param timestamp: Time data was received.
        :return: ID of inserted row.
        """

        # If timestamp is not provided default to now.
        if timestamp == 0:
            timestamp = datetime.now().timestamp()

        date_object = datetime.fromtimestamp(timestamp)

        # Get the raw data.
        grid_data = SolarData.get_grid_data()
        inverter_data = SolarData.get_inverter_data()

        # Prepare data object to be stored in database.
        store_data = {
            'grid_power_usage_real': grid_data['grid_power_usage_real'],
            'grid_power_factor': grid_data['grid_power_factor'],
            'grid_power_apparent': grid_data['grid_power_apparent'],
            'grid_power_reactive': grid_data['grid_power_reactive'],
            'grid_ac_voltage': grid_data['grid_ac_voltage'],
            'grid_ac_current': grid_data['grid_ac_current'],
            'inverter_ac_frequency': inverter_data['inverter_ac_frequency'],
            'inverter_ac_current': inverter_data['inverter_ac_current'],
            'inverter_ac_voltage': inverter_data['inverter_ac_voltage'],
            'inverter_ac_power': inverter_data['inverter_ac_power'],
            'inverter_dc_current': inverter_data['inverter_dc_current'],
            'inverter_dc_voltage': inverter_data['inverter_dc_voltage'],
            'time_stamp': timestamp,
            'time_year': date_object.year,
            'time_month': date_object.month,
            'time_day': date_object.day
        }

        # Store data in the database.
        data_record = SolarDataModel(**store_data)
        data_record.save()

        # Return ID of inserted row.
        return data_record.id
