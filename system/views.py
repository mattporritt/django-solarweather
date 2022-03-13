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

from django.shortcuts import render
from django.http import HttpResponseNotAllowed, JsonResponse
from weather.weatherdata import WeatherData
from solar.solardata import SolarData
from datetime import datetime
import logging

# Get an instance of a logger
logger = logging.getLogger('django')


def weather_dashboard(request):
    """
    This is the view that render the weather dashboard.
    :param request:
    :return:
    """

    context = {}

    # Pass the context to a template
    return render(request, 'system/index.html', context)


def weather_history(request):
    """
    This is the view that render the weather history.
    :param request:
    :return:
    """

    weather_data = WeatherData()
    context = weather_data.get_date_range()

    # Pass the context to a template
    return render(request, 'system/history.html', context)


def solar_dashboard(request):
    """
    This is the view that render the solar dashboard.
    :param request:
    :return:
    """

    context = {}

    # Pass the context to a template
    return render(request, 'system/solar.html', context)


def solar_history(request):
    """
    This is the view that render the solar history.
    :param request:
    :return:
    """

    solar_data = SolarData()
    context = solar_data.get_date_range()

    # Pass the context to a template
    return render(request, 'system/solar_history.html', context)


def data_ajax(request):
    """
    This view handles ajax requests for the main dashboard.

    :param request:
    :return:
    """

    if request.method == 'POST':
        return HttpResponseNotAllowed(['GET'])
    elif request.method == 'GET':
        # If timestamp is not provided default to now.
        timestamp = int(request.GET.get('timestamp', default=0))
        if timestamp == 0:
            timestamp = datetime.now().timestamp()

        # Decide which dataset we are getting.
        dashboard = str(request.GET.get('dashboard', default='weather'))

        # Decide if we are getting historic data.
        history = int(request.GET.get('history', default=0))

        if dashboard == 'weather':
            weather_data = WeatherData()
            if history == 1:
                result_data = weather_data.get_history(timestamp)
            else:
                result_data = weather_data.get_data(timestamp)
        elif dashboard == 'solar':
            solar_data = SolarData()
            if history == 1:
                result_data = solar_data.get_history(timestamp)
            else:
                result_data = solar_data.get_data(timestamp)

        response = JsonResponse(result_data)
        return response
