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

from weather.models import WeatherData as WeatherDataModel
from system.conversion import UnitConversion


class WeatherData:
    """
    Class to weather station data related operations
    """

    def store(self, data: dict) -> int:
        """
        Store received weather station data into database.
        :param data:
        :return:
        """

        store_data = {
            'indoor_temp': UnitConversion.f_to_c(float(data.get('indoortempf'))),
            'outdoor_temp': UnitConversion.f_to_c(float(data.get('tempf'))),
            'dew_point': UnitConversion.f_to_c(float(data.get('dewptf'))),
            'wind_chill': UnitConversion.f_to_c(float(data.get('windchillf'))),
            'indoor_humidity': float(data.get('indoorhumidity')),
            'outdoor_humidity': float(data.get('humidity')),
            'wind_speed': UnitConversion.mph_to_kmh(float(data.get('windspeedmph'))),
            'wind_gust': UnitConversion.mph_to_kmh(float(data.get('windgustmph'))),
            'wind_direction': float(data.get('winddir')),
            'absolute_pressure': UnitConversion.inhg_to_hpa(float(data.get('absbaromin'))),
            'pressure': UnitConversion.inhg_to_hpa(float(data.get('baromin'))),
            'rain': UnitConversion.in_to_cm(float(data.get('rainin'))),
            'daily_rain': UnitConversion.in_to_cm(float(data.get('dailyrainin'))),
            'weekly_rain': UnitConversion.in_to_cm(float(data.get('weeklyrainin'))),
            'monthly_rain': UnitConversion.in_to_cm(float(data.get('monthlyrainin'))),
            'solar_radiation': float(data.get('solarradiation')),
            'uv_index': int(data.get('UV')),
            'date_utc': data.get('dateutc'),
            'software_type': data.get('softwaretype'),
            'action': data.get('action'),
            'real_time': int(data.get('realtime')),
            'radio_freq': int(data.get('rtfreq')),
        }

        data_record = WeatherDataModel(**store_data)

        data_record.save()

        return data_record.id




