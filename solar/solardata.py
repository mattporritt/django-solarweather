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
        grid_data = request_response.json()

        # TODO: Filter out unwanted data.

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
        inverter_data = request_response.json(

        # TODO: Filter out unwanted data.
        # TODO: handle missing elements.

        return inverter_data
