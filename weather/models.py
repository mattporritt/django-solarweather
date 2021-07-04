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

from django.db import models

class WeatherData(models.Model):
    """
    This model stores the data received from the weather station.
    """
    indoor_temp=models.DecimalField(max_digits=3, decimal_places=3)
    outdoor_temp=models.DecimalField(max_digits=3, decimal_places=3)
    dew_point=models.DecimalField(max_digits=3, decimal_places=3)
    wind_chill=models.DecimalField(max_digits=3, decimal_places=3)
    indoor_humidity=models.DecimalField(max_digits=3, decimal_places=3)
    outdoor_humidity=models.DecimalField(max_digits=3, decimal_places=3)
    wind_speed=models.DecimalField(max_digits=3, decimal_places=3)
    wind_gust=models.DecimalField(max_digits=3, decimal_places=3)
    wind_direction=models.DecimalField(max_digits=3, decimal_places=3)
    absolute_pressure=models.DecimalField(max_digits=3, decimal_places=3)
    pressure=models.DecimalField(max_digits=3, decimal_places=3)
    rain=models.DecimalField(max_digits=3, decimal_places=3)
    daily_rain=models.DecimalField(max_digits=3, decimal_places=3)
    weekly_rain=models.DecimalField(max_digits=3, decimal_places=3)
    monthly_rain=models.DecimalField(max_digits=3, decimal_places=3)
    solar_radiation=models.DecimalField(max_digits=3, decimal_places=3)
    uv_index=models.IntegerField()
    date_utc=models.DateTimeField()
    software_type=models.CharField(max_length=100)
    action=models.CharField(max_length=100)
    real_time=models.IntegerField()
    radio_freq=models.IntegerField()
