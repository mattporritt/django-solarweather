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
from django.db.models import Max, Min
from system.conversion import UnitConversion
from datetime import datetime
from django.utils.timezone import make_aware


class WeatherData:
    """
    Class to weather station data related operations
    """

    @staticmethod
    def store(data: dict) -> int:
        """
        Store received weather station data into database.
        :param data:
        :return:
        """

        # First do some date mangling.
        date_string = data.get('dateutc').replace('%20', ' ')
        datetime_object = make_aware(datetime.strptime(date_string, '%Y-%m-%d %X'))

        # Prepare data object to be stored in database.
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
            'date_utc': datetime_object,
            'time_stamp': datetime_object.timestamp(),
            'time_year': datetime_object.year,
            'time_month': datetime_object.month,
            'time_day': datetime_object.day,
            'software_type': data.get('softwaretype'),
            'action': data.get('action'),
            'real_time': int(data.get('realtime')),
            'radio_freq': int(data.get('rtfreq')),
        }

        # Store data in the database.
        data_record = WeatherDataModel(**store_data)
        data_record.save()

        # Return ID of inserted row.
        return data_record.id

    @staticmethod
    def get_max(metric: str, period: str, timestamp: int = 0):
        """
        Get the maximum value for a given time period.

        :param metric: The metric to get the maximum for, e.g. uv_index
        :param period: The period the maximum relates to. i.e. 'year', 'month', 'day'.
        :param timestamp: The unix timestamp to use as the reference.
        :return: The found maximum value.
        """

        # If timestamp is not provided default to now.
        if timestamp == 0:
            timestamp = datetime.now().timestamp()

        # Split out timestamp to date components.
        date_object = datetime.fromtimestamp(timestamp)
        max_year = date_object.year
        max_month = date_object.month
        max_day = date_object.day

        max_value = {}

        # Get value from cache.
        # If cache is empty or invalid get value from the database. Then store in cache.
        if period == 'year':
            max_value = WeatherDataModel.objects\
                .filter(date_utc__year=max_year)\
                .aggregate(Max(metric))
        elif period == 'month':
            max_value = WeatherDataModel.objects \
                .filter(date_utc__year=max_year, date_utc__month=max_month) \
                .aggregate(Max(metric))
        elif period == 'day':
            max_value = WeatherDataModel.objects \
                .filter(date_utc__year=max_year, date_utc__month=max_month, date_utc__day=max_day) \
                .aggregate(Max(metric))

        return max_value

    def set_max(self, metric: str, period: str):
        """
        Set the maximum value for a given time period.

        :param metric:
        :param period:
        :return:
        """

    @staticmethod
    def get_min(metric: str, period: str, timestamp: int = 0):
        """
        Get the minimum value for a given time period.

        :param metric: The metric to get the minimum for, e.g. uv_index
        :param period: The period the minimum relates to. i.e. 'year', 'month', 'day'.
        :param timestamp: The unix timestamp to use as the reference.
        :return: The found minimum value.
        """

        # If timestamp is not provided default to now.
        if timestamp == 0:
            timestamp = datetime.now().timestamp()

        # Split out timestamp to date components.
        date_object = datetime.fromtimestamp(timestamp)
        min_year = date_object.year
        min_month = date_object.month
        min_day = date_object.day

        min_value = {}

        # Get value from cache.
        # If cache is empty or invalid get value from the database. Then store in cache.
        if period == 'year':
            min_value = WeatherDataModel.objects\
                .filter(date_utc__year=min_year)\
                .aggregate(Min(metric))
        elif period == 'month':
            min_value = WeatherDataModel.objects \
                .filter(date_utc__year=min_year, date_utc__month=min_month) \
                .aggregate(Min(metric))
        elif period == 'day':
            min_value = WeatherDataModel.objects \
                .filter(date_utc__year=min_year, date_utc__month=min_month, date_utc__day=min_day) \
                .aggregate(Min(metric))

        return min_value

    def set_min(self, metric: str, period: str):
        """
        Set the minimum value for a given time period.

        :param metric:
        :param period:
        :return:
        """

    def get_data(self):
        """
        Get all the data needed to display the weather dashboard.
        Data returned:
            Indoor temp - current, daily max, daily min.
            Outdoor temp - current, daily max, daily min.


        :return:
        """
