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
from psqlextra.backend.migrations.operations import PostgresAddRangePartition

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

class Migration(migrations.Migration):
    """
    Set up the initial partitions
    """
    operations = [
        PostgresAddRangePartition(
            model_name="SolarData",
            name="weather_weatherdata_2021_08",
            from_values="1628702487",
            to_values="1630418353",
        ),
        PostgresAddRangePartition(
            model_name="SolarData",
            name="weather_weatherdata_2021_09",
            from_values="1630418423",
            to_values="1633010364",
        ),
        PostgresAddRangePartition(
            model_name="SolarData",
            name="weather_weatherdata_2021_10",
            from_values="1633010432",
            to_values="1635685171",
        ),
        PostgresAddRangePartition(
            model_name="SolarData",
            name="weather_weatherdata_2021_11",
            from_values="1635685243",
            to_values="1638277180",
        ),
        PostgresAddRangePartition(
            model_name="SolarData",
            name="weather_weatherdata_2021_12",
            from_values="1638277251",
            to_values="1640955588",
        ),
        PostgresAddRangePartition(
            model_name="SolarData",
            name="weather_weatherdata_2022_01",
            from_values="1640955658",
            to_values="1643633997",
        ),
        PostgresAddRangePartition(
            model_name="SolarData",
            name="weather_weatherdata_2022_02",
            from_values="1643634000",
            to_values="1645966800",
        ),
    ]