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
from django.core.cache import cache
import math


class WeatherData:
    """
    Class to weather station data related operations
    """

    # Metrics we can query and get data for.
    weather_metrics = [
        'indoor_temp',
        'outdoor_temp',
        'indoor_feels_temp',
        'outdoor_feels_temp',
        'indoor_dew_temp',
        'outdoor_dew_temp',
        'dew_point',
        'wind_chill',
        'indoor_humidity',
        'outdoor_humidity',
        'wind_speed',
        'wind_gust',
        'wind_direction',
        'absolute_pressure',
        'pressure',
        'rain',
        'daily_rain',
        'weekly_rain',
        'monthly_rain',
        'solar_radiation',
        'uv_index',
    ]

    # Metrics to get trend data for.
    weather_trends = [
        'indoor_temp',
        'outdoor_temp',
        'indoor_feels_temp',
        'outdoor_feels_temp',
        'indoor_dew_temp',
        'outdoor_dew_temp',
        'dew_point',
        'wind_chill',
        'indoor_humidity',
        'outdoor_humidity',
        'wind_speed',
        'wind_gust',
        'wind_direction',
        'absolute_pressure',
        'pressure',
        'rain',
        'daily_rain',
        'solar_radiation',
        'uv_index',
    ]

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

        # We reuse some values that need post processing first
        indoor_temp = UnitConversion.f_to_c(float(data.get('indoortempf')))
        outdoor_temp = UnitConversion.f_to_c(float(data.get('tempf')))
        indoor_humidity = float(data.get('indoorhumidity'))
        outdoor_humidity = float(data.get('humidity'))
        wind_speed = UnitConversion.mph_to_kmh(float(data.get('windspeedmph')))
        solar_radiation = float(data.get('solarradiation'))

        # Prepare data object to be stored in database.
        store_data = {
            'indoor_temp': indoor_temp,
            'outdoor_temp': outdoor_temp,
            'indoor_feels_temp': WeatherData.get_apparent_temperature(indoor_temp, indoor_humidity, wind_speed, solar_radiation),
            'outdoor_feels_temp': WeatherData.get_apparent_temperature(outdoor_temp, outdoor_humidity, 0.1, 0),
            'indoor_dew_temp': WeatherData.get_dew_point(indoor_temp, indoor_humidity),
            'outdoor_dew_temp': WeatherData.get_dew_point(outdoor_temp, outdoor_humidity),
            'dew_point': UnitConversion.f_to_c(float(data.get('dewptf'))),
            'wind_chill': UnitConversion.f_to_c(float(data.get('windchillf'))),
            'indoor_humidity': indoor_humidity,
            'outdoor_humidity': outdoor_humidity,
            'wind_speed': wind_speed,
            'wind_gust': UnitConversion.mph_to_kmh(float(data.get('windgustmph'))),
            'wind_direction': float(data.get('winddir')),
            'absolute_pressure': UnitConversion.inhg_to_hpa(float(data.get('absbaromin'))),
            'pressure': UnitConversion.inhg_to_hpa(float(data.get('baromin'))),
            'rain': UnitConversion.in_to_cm(float(data.get('rainin'))),
            'daily_rain': UnitConversion.in_to_cm(float(data.get('dailyrainin'))),
            'weekly_rain': UnitConversion.in_to_cm(float(data.get('weeklyrainin'))),
            'monthly_rain': UnitConversion.in_to_cm(float(data.get('monthlyrainin'))),
            'solar_radiation': solar_radiation,
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

        # Update max and min values.
        for metric, value in store_data.items():
            if (type(value) is int) or (type(value) is float):
                WeatherData.set_max(metric, 'day', value, store_data['time_stamp'])
                WeatherData.set_min(metric, 'day', value, store_data['time_stamp'])
                WeatherData.set_latest(metric, value)

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
        metric_max = '{0}__max'.format(metric)

        # Get value from cache.
        # If cache is empty or invalid get value from the database. Then store in cache.
        if period == 'year':
            cache_key = '_'.join((metric, str(max_year)))
            cache_val = cache.get(cache_key)
            if cache_val is None:
                max_value = WeatherDataModel.objects\
                    .filter(date_utc__year=max_year)\
                    .aggregate(Max(metric))
                if max_value[metric_max] is None:
                    max_value = {metric_max: 0}
            else:
                max_value = {metric_max: cache_val}
        elif period == 'month':
            cache_key = '_'.join((metric, str(max_year), str(max_month)))
            cache_val = cache.get(cache_key)
            if cache_val is None:
                max_value = WeatherDataModel.objects \
                    .filter(date_utc__year=max_year, date_utc__month=max_month) \
                    .aggregate(Max(metric))
                if max_value[metric_max] is None:
                    max_value = {metric_max: 0}
            else:
                max_value = {metric_max: cache_val}
        elif period == 'day':
            cache_key = '_'.join((metric, str(max_year), str(max_month), str(max_day)))
            cache_val = cache.get(cache_key)
            if cache_val is None:
                max_value = WeatherDataModel.objects \
                    .filter(date_utc__year=max_year, date_utc__month=max_month, date_utc__day=max_day) \
                    .aggregate(Max(metric))
                if max_value[metric_max] is None:
                    max_value = {metric_max: 0}
            else:
                max_value = {metric_max: cache_val}
        return max_value

    @staticmethod
    def set_max(metric: str, period: str, value, timestamp: int = 0):
        """
        Set the maximum value for a given time period.
        The value is only "set" in the cache and not updated in the database.
        max values are not stored explicitly in the database but are resolved
        from all stored values.

        :param metric: The metric to get the maximum for, e.g. uv_index
        :param period: The period the maximum relates to. i.e. 'year', 'month', 'day'.
        :param value: The new maximum value.
        :param timestamp: The unix timestamp to use as the reference.
        :return:
        """

        # If timestamp is not provided default to now.
        if timestamp == 0:
            timestamp = datetime.now().timestamp()

        current_max = WeatherData.get_max(metric, period, timestamp)
        max_metric = ''.join((metric, '__max'))

        if current_max.get(max_metric) >= value:
            # New max is not greater nothing to do.
            max_set = False
        else:
            # New max is greater update cache with new value.

            # Split out timestamp to date components.
            date_object = datetime.fromtimestamp(timestamp)
            max_year = date_object.year
            max_month = date_object.month
            max_day = date_object.day

            if period == 'year':
                cache_key = '_'.join((metric, str(max_year)))

            elif period == 'month':
                cache_key = '_'.join((metric, str(max_year), str(max_month)))
                # If there is a new month max, there may also be a new year max.
                # We use recursion (magic) to check.
                result = WeatherData.set_max(metric, 'year', value, timestamp)

            elif period == 'day':
                cache_key = '_'.join((metric, str(max_year), str(max_month), str(max_day)))
                # If there is a new day max, there may be a new month max.
                WeatherData.set_max(metric, 'month', value, timestamp)

            cache.set(cache_key, value, 3600)
            max_set = True

        return max_set

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
        metric_min = '{0}__min'.format(metric)

        # Get value from cache.
        # If cache is empty or invalid get value from the database. Then store in cache.
        if period == 'year':
            cache_key = '_'.join((metric, str(min_year)))
            cache_val = cache.get(cache_key)
            if cache_val is None:
                min_value = WeatherDataModel.objects\
                    .filter(date_utc__year=min_year)\
                    .aggregate(Min(metric))
                if min_value[metric_min] is None:
                    min_value = {metric_min: 0}
            else:
                min_value = {metric_min: cache_val}
        elif period == 'month':
            cache_key = '_'.join((metric, str(min_year), str(min_month)))
            cache_val = cache.get(cache_key)
            if cache_val is None:
                min_value = WeatherDataModel.objects \
                    .filter(date_utc__year=min_year, date_utc__month=min_month) \
                    .aggregate(Min(metric))
                if min_value[metric_min] is None:
                    min_value = {metric_min: 0}
            else:
                min_value = {metric_min: cache_val}
        elif period == 'day':
            cache_key = '_'.join((metric, str(min_year), str(min_month), str(min_day)))
            cache_val = cache.get(cache_key)
            if cache_val is None:
                min_value = WeatherDataModel.objects \
                    .filter(date_utc__year=min_year, date_utc__month=min_month, date_utc__day=min_day) \
                    .aggregate(Min(metric))
                if min_value[metric_min] is None:
                    min_value = {metric_min: 0}
            else:
                min_value = {metric_min: cache_val}
        return min_value

    @staticmethod
    def set_min(metric: str, period: str, value, timestamp: int = 0) -> bool:
        """
        Set the minimum value for a given time period.
        The value is only "set" in the cache and not updated in the database.
        min values are not stored explicitly in the database but are resolved
        from all stored values.

        :param metric: The metric to get the minimum for, e.g. uv_index
        :param period: The period the minimum relates to. i.e. 'year', 'month', 'day'.
        :param value: The new minimum value.
        :param timestamp: The unix timestamp to use as the reference.
        :return:
        """

        # If timestamp is not provided default to now.
        if timestamp == 0:
            timestamp = datetime.now().timestamp()

        current_min = WeatherData.get_min(metric, period, timestamp)
        min_metric = ''.join((metric, '__min'))

        if current_min.get(min_metric) <= value:
            # New min is not greater nothing to do.
            min_set = False
        else:
            # New min is greater update cache with new value.

            # Split out timestamp to date components.
            date_object = datetime.fromtimestamp(timestamp)
            min_year = date_object.year
            min_month = date_object.month
            min_day = date_object.day

            if period == 'year':
                cache_key = '_'.join((metric, str(min_year)))

            elif period == 'month':
                cache_key = '_'.join((metric, str(min_year), str(min_month)))
                # If there is a new month min, there may also be a new year min.
                # We use recursion (magic) to check.
                result = WeatherData.set_min(metric, 'year', value, timestamp)

            elif period == 'day':
                cache_key = '_'.join((metric, str(min_year), str(min_month), str(min_day)))
                # If there is a new day min, there may be a new month min.
                WeatherData.set_min(metric, 'month', value, timestamp)

            cache.set(cache_key, value, 3600)
            min_set = True

        return min_set

    @staticmethod
    def get_latest(metric: str) -> dict:
        """
        Get the latest received value for a metric

        :param: metric: The metric to set the latest for, e.g. uv_index
        :return:
        """

        cache_key = '{0}_latest'.format(metric)
        cache_val = cache.get(cache_key)

        return {cache_key: cache_val}

    @staticmethod
    def set_latest(metric: str, value) -> dict:
        """
        Set the latest value for a given metric.
        The value is only "set" in the cache and not updated in the database.

        :param metric: The metric to set the latest for, e.g. uv_index
        :param value: The latest value.
        :return:
        """

        cache_key = '{0}_latest'.format(metric)
        cache.set(cache_key, value, 3600)

        return {cache_key: value}

    @staticmethod
    def get_apparent_temperature(temp: float, humidity: float, wind: float, solar: float) -> float:
        """
        This method returns the Australian Apparent Temperature (AT),
        otherwise known as the "feels like" temperature.

        The formula used for the AT is the same as the one used by the
        Australian Bureau of Meteorology. It is an approximations of the
        value provided by a mathematical model of heat balance in the human body.
        It can includes the effects of temperature, humidity and wind-speed.
        If present it will also take into account solar radiation.

        :param temp: Temperature in degrees celsius.
        :param humidity: Percent relative humidity, e.g. 88(%).
        :param wind: Wind speed in kilometers per hour.
        :param solar: Net radiation absorbed per unit area of body surface (w/m2).
        :return:
        """

        # First convert wind speed from km/h to m/s.
        windms = wind / 3.6

        # Next calculate water vapour pressure.
        # This can be calculated from the temperature and relative humidity.
        exponent_val = (17.27 * temp) / (237.7 + temp)
        vapour = (humidity / 100) * 6.105 * (math.exp(exponent_val))

        # The algorithm is adjusted depending on if we have solar radiation or not.
        if solar > 0:
            at = temp + (0.348 * vapour) - (0.70 * windms) + ((0.70 * solar) / (windms + 10)) - 4.25
        else:
            at = temp + (0.348 * vapour) - (0.70 * windms) - 4.00

        return round(at, 3)

    @staticmethod
    def get_dew_point(temp: float, humidity: float) -> float:
        """
        Calculate the dew point temperature from temp and
        relative humidity.

        :param temp: Temperature in degrees celsius.
        :param humidity: Percent relative humidity, e.g. 88(%).
        :return:
        """

        ln_humid = math.log(humidity / 100)
        k_temp = 243.04 + temp

        dew_point = 243.04 * (ln_humid + ((17.625 * temp) / k_temp)) / (17.625 - ln_humid - ((17.625 * temp) / k_temp))

        return round(dew_point, 3)

    @staticmethod
    def get_data(timestamp: int = 0) -> dict:
        """
        Get all the data needed to display the weather dashboard.
        Data returned for all metrics:
            latest, daily max, daily min,
            monthly max, monthly min,
            yearly max, yearly min.

        :return:
        """

        # If timestamp is not provided default to now.
        if timestamp == 0:
            timestamp = datetime.now().timestamp()

        result_data = {}

        for metric in WeatherData.weather_metrics:
            result_data[metric] = {}
            result_data[metric]['latest'] = WeatherData.get_latest(metric).get('{0}_latest'.format(metric))
            result_data[metric]['daily_max'] = WeatherData.get_max(metric, 'day', timestamp).get('{0}__max'.format(metric))
            result_data[metric]['daily_min'] = WeatherData.get_min(metric, 'day', timestamp).get('{0}__min'.format(metric))
            result_data[metric]['monthly_max'] = WeatherData.get_max(metric, 'month', timestamp).get('{0}__max'.format(metric))
            result_data[metric]['monthly_min'] = WeatherData.get_min(metric, 'month', timestamp).get('{0}__min'.format(metric))
            result_data[metric]['yearly_max'] = WeatherData.get_max(metric, 'year', timestamp).get('{0}__max'.format(metric))
            result_data[metric]['yearly_min'] = WeatherData.get_min(metric, 'year', timestamp).get('{0}__min'.format(metric))

            for trend in WeatherData.weather_trends:
                result_data[metric]['daily_trend'] = list(WeatherData.get_trend(metric, 'day', timestamp))

        return result_data

    @staticmethod
    def get_trend(metric: str, period: str, timestamp: int = 0) -> dict:
        """
        Get the metric trend data for a given time period.

        :param metric: The metric to get the trend for, e.g. indoor_temp
        :param period: The period the trend relates to. i.e. 'year', 'month', 'day'.
        :param timestamp: The unix timestamp to use as the reference.
        :return: The trend data.
        """

        # If timestamp is not provided default to now.
        if timestamp == 0:
            timestamp = datetime.now().timestamp()

        # Split out timestamp to date components.
        date_object = datetime.fromtimestamp(timestamp)
        trend_year = date_object.year
        trend_month = date_object.month
        trend_day = date_object.day

        trend_data = {}

        # TODO: decide if this needs to be cached.
        if period == 'year':
            trend_data = WeatherDataModel.objects.values_list('time_stamp', metric) \
                .filter(date_utc__year=trend_year) \
                .order_by('time_stamp') \
                .all()
        elif period == 'month':
            trend_data = WeatherDataModel.objects.values_list('time_stamp', metric) \
                .filter(date_utc__year=trend_year, date_utc__month=trend_month) \
                .order_by('time_stamp') \
                .all()
        elif period == 'day':
            trend_data = WeatherDataModel.objects.values_list('time_stamp', metric) \
                .filter(date_utc__year=trend_year, date_utc__month=trend_month, date_utc__day=trend_day) \
                .order_by('time_stamp') \
                .all()

        return trend_data
