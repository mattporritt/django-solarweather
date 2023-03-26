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

from django.core.management.base import BaseCommand, CommandError
from weather.weatherdata import WeatherData
import paho.mqtt.client as mqtt
from django.conf import settings


class Command(BaseCommand):
    help = 'Publishes data to the MQTT queue'

    def mqtt_connect(self):
        # Set up the MQTT connection
        mqtt_client = mqtt.Client('solarweather')
        mqtt_client.tls_set()
        mqtt_client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASS)
        mqtt_client.connect(settings.MQTT_HOST)
        return mqtt_client

    def handle(self, *args, **options):
        # Set up the MQTT connection
        mqtt_client = mqtt.Client('solarweather')
        mqtt_client.tls_set()

        outdoor_temp = WeatherData.get_latest('outdoor_temp')
        wind_speed = WeatherData.get_latest('wind_speed')
        pressure = WeatherData.get_latest('pressure')
        self.stdout.write('{}\n'.format(outdoor_temp))
