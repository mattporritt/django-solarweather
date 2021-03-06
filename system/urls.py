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

"""
SolarWeather System App URL Configuration.

"""
from django.urls import path, re_path

from system import views

urlpatterns = [
    path('', views.weather_dashboard, name='weather.dashboard'),
    re_path(r'^history[\/]?', views.weather_history, name='weather_history'),
    re_path(r'^solar\/history[\/]?', views.solar_history, name='solar_history'),
    re_path(r'^solar[\/]?', views.solar_dashboard, name='solar_dashboard'),
    re_path(r'^dataajax\/.*', views.data_ajax, name='data_ajax'),
]