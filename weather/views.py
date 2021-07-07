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

from django.http import HttpResponse
from models import WeatherData
import logging

# Get an instance of a logger
logger = logging.getLogger('django')


def index(request):
    logger.info(request.environ.get('REMOTE_ADDR', '0.0.0.0'))
    logger.info(request.GET.get('ID'))
    

    response = HttpResponse()
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    response.content = 'success'

    # Return a simple response
    return response

