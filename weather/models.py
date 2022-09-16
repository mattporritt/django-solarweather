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

from django.db import migrations, models
from psqlextra.types import PostgresPartitioningMethod
from psqlextra.models import PostgresPartitionedModel

class WeatherData(PostgresPartitionedModel):
    """
    This model stores the data received from the weather station.
    """
    class PartitioningMeta:
        method = PostgresPartitioningMethod.RANGE
        key = ['time_stamp']

    indoor_temp = models.FloatField()
    outdoor_temp = models.FloatField()
    indoor_feels_temp = models.FloatField()
    outdoor_feels_temp = models.FloatField()
    indoor_dew_temp = models.FloatField()
    outdoor_dew_temp = models.FloatField()
    dew_point = models.FloatField()
    wind_chill = models.FloatField()
    indoor_humidity = models.FloatField()
    outdoor_humidity = models.FloatField()
    wind_speed = models.FloatField()
    wind_gust = models.FloatField()
    wind_direction = models.FloatField()
    absolute_pressure = models.FloatField()
    pressure = models.FloatField()
    rain = models.FloatField()
    daily_rain = models.FloatField()
    weekly_rain = models.FloatField()
    monthly_rain = models.FloatField()
    solar_radiation = models.FloatField()
    uv_index = models.IntegerField()
    date_utc = models.DateTimeField()
    time_stamp = models.IntegerField(db_index=True)
    time_year = models.IntegerField(db_index=True)
    time_month = models.IntegerField(db_index=True)
    time_day = models.IntegerField(db_index=True)
    software_type = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    real_time = models.IntegerField()
    radio_freq = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['indoor_temp', 'time_year']),
            models.Index(fields=['outdoor_temp', 'time_year']),
            models.Index(fields=['indoor_feels_temp', 'time_year']),
            models.Index(fields=['outdoor_feels_temp', 'time_year']),
            models.Index(fields=['indoor_dew_temp', 'time_year']),
            models.Index(fields=['outdoor_dew_temp', 'time_year']),
            models.Index(fields=['dew_point', 'time_year']),
            models.Index(fields=['wind_chill', 'time_year']),
            models.Index(fields=['indoor_humidity', 'time_year']),
            models.Index(fields=['outdoor_humidity', 'time_year']),
            models.Index(fields=['wind_speed', 'time_year']),
            models.Index(fields=['wind_gust', 'time_year']),
            models.Index(fields=['wind_direction', 'time_year']),
            models.Index(fields=['absolute_pressure', 'time_year']),
            models.Index(fields=['pressure', 'time_year']),
            models.Index(fields=['rain', 'time_year']),
            models.Index(fields=['daily_rain', 'time_year']),
            models.Index(fields=['weekly_rain', 'time_year']),
            models.Index(fields=['monthly_rain', 'time_year']),
            models.Index(fields=['solar_radiation', 'time_year']),
            models.Index(fields=['uv_index', 'time_year']),
        ]
