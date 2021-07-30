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
from django.http import HttpResponse
from weather.weatherdata import WeatherData
import logging

# Get an instance of a logger
logger = logging.getLogger('django')


def dashboard(request):
    """
    This is the view that render the main dashboard.
    :param request:
    :return:
    """

    context = {}

    # Pass the context to a template
    return render(request, 'system/index.html', context)


def data_ajax(request):
    """
    This view handles ajax requests for the main dashboard.

    :param request:
    :return:
    """

    response = HttpResponse()
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    response.content = 'success'

    # Return a simple response
    return response

