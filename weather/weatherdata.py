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
from django.conf import settings
from django.core.cache import cache
import math
import pytz

import logging

# Get an instance of a logger
logger = logging.getLogger('django')


class WeatherData:
    """
    Class to get weather station data and related operations.
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
    ]

    @staticmethod
    def store(data: dict) -> int:
        """
        Store received weather station data into database.

        :param data: Data received from the weather station
        :return: ID of inserted row.
        """

        # First do some date mangling.
        tz = pytz.timezone(getattr(settings, 'TIME_ZONE'))
        date_string = data.get('dateutc').replace('%20', ' ')
        utc_time = datetime.strptime(date_string, '%Y-%m-%d %X')
        datetime_object = pytz.utc.localize(utc_time, is_dst=None).astimezone(tz)

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
            'indoor_feels_temp': WeatherData.get_apparent_temperature(indoor_temp, indoor_humidity, 0.1, 0),
            'outdoor_feels_temp': WeatherData.get_apparent_temperature(outdoor_temp, outdoor_humidity, wind_speed, 0),
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
            'rain': UnitConversion.in_to_mm(float(data.get('rainin'))),
            'daily_rain': UnitConversion.in_to_mm(float(data.get('dailyrainin'))),
            'weekly_rain': UnitConversion.in_to_mm(float(data.get('weeklyrainin'))),
            'monthly_rain': UnitConversion.in_to_mm(float(data.get('monthlyrainin'))),
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

        # Update latest, max and min values.
        timestamp = datetime.now().timestamp()
        date_object = datetime.fromtimestamp(timestamp)
        time_obj = {
            'year': date_object.year,
            'month': date_object.month,
            'day': date_object.day
        }
        for metric, value in store_data.items():
            if (type(value) is int) or (type(value) is float):
                WeatherData.set_max(metric, 'day', value, time_obj)
                WeatherData.set_min(metric, 'day', value, time_obj)
                WeatherData.set_latest(metric, value)

        # Store data in the database.
        data_record = WeatherDataModel(**store_data)
        data_record.save()

        # Return ID of inserted row.
        return data_record.id

    @staticmethod
    def get_max(metric: str, period: str, time_obj: dict, usecache: bool = True):
        """
        Get the maximum value for a given time period.

        :param metric: The metric to get the maximum for, e.g. uv_index
        :param period: The period the maximum relates to. i.e. 'year', 'month', 'day'.
        :param time_obj: The object that contains the time data.
        :param usecache: Use max value from cache. False means get from database.
        :return: The found maximum value.
        """

        max_year = time_obj['year']
        max_month = time_obj['month']
        max_day = time_obj['day']
        tz = pytz.timezone(getattr(settings, 'TIME_ZONE'))

        max_value = {}
        metric_max = '{0}__max'.format(metric)

        # Get value from cache.
        # If cache is empty or invalid get value from the database. Then store in cache.
        if period == 'year':
            cache_key = '_'.join(('max', metric, str(max_year)))
            cache_val = cache.get(cache_key)
            if (cache_val is None) or (usecache is False):
                year_stamp = datetime(max_year,1,1,0,0,0, tzinfo=tz).timestamp()
                max_value = WeatherDataModel.objects\
                    .filter(time_year=max_year, time_stamp__gte=year_stamp)\
                    .aggregate(Max(metric))
                if max_value[metric_max] is None:
                    max_value = {metric_max: 0}
            else:
                max_value = {metric_max: cache_val}
        elif period == 'month':
            cache_key = '_'.join(('max', metric, str(max_year), str(max_month)))
            cache_val = cache.get(cache_key)
            if (cache_val is None) or (usecache is False):
                month_stamp = datetime(max_year, max_month, 1, 0, 0, 0, tzinfo=tz).timestamp()
                max_value = WeatherDataModel.objects \
                    .filter(time_year=max_year, time_month=max_month, time_stamp__gte=month_stamp) \
                    .aggregate(Max(metric))
                if max_value[metric_max] is None:
                    max_value = {metric_max: 0}
            else:
                max_value = {metric_max: cache_val}
        elif period == 'day':
            cache_key = '_'.join(('max', metric, str(max_year), str(max_month), str(max_day)))
            cache_val = cache.get(cache_key)
            if (cache_val is None) or (usecache is False):
                day_stamp = datetime(max_year, max_month, max_day, 0, 0, 0, tzinfo=tz).timestamp()
                max_value = WeatherDataModel.objects \
                    .filter(time_year=max_year, time_month=max_month, time_day=max_day, time_stamp__gte=day_stamp) \
                    .aggregate(Max(metric))
                if max_value[metric_max] is None:
                    max_value = {metric_max: 0}
            else:
                max_value = {metric_max: cache_val}
        return max_value

    @staticmethod
    def set_max(metric: str, period: str, value, time_obj: dict):
        """
        Set the maximum value for a given time period.
        The value is only "set" in the cache and not updated in the database.
        max values are not stored explicitly in the database but are resolved
        from all stored values.

        :param metric: The metric to get the maximum for, e.g. uv_index
        :param period: The period the maximum relates to. i.e. 'year', 'month', 'day'.
        :param value: The new maximum value.
        :param time_obj: The object that contains the time data.
        :return:
        """

        max_year = time_obj['year']
        max_month = time_obj['month']
        max_day = time_obj['day']
        max_set = False

        # Abort early if metric is not in allowed list
        if metric not in WeatherData.weather_metrics:
            return

        if period == 'year':
            cache_key = '_'.join(('max', metric, str(max_year)))

        elif period == 'month':
            cache_key = '_'.join(('max', metric, str(max_year), str(max_month)))

        elif period == 'day':
            cache_key = '_'.join(('max', metric, str(max_year), str(max_month), str(max_day)))

        cache_val = cache.get(cache_key)  # Raw check of cache.
        if cache_val is None:
            # Cache is empty, get value from database.
            db_val = WeatherData.get_max(metric, period, time_obj, False)
            max_metric = ''.join((metric, '__max'))
            cache_val = db_val.get(max_metric)
            cache.set(cache_key, cache_val, 3600)
            max_set = True

        if cache_val < value:
            cache.set(cache_key, value, 3600)
            max_set = True

        # Do recursive checks if needed.
        if period == 'month' and max_set is True:
            # If there is a new month max, there may also be a new year max.
            # We use recursion (magic) to check.
            WeatherData.set_max(metric, 'year', value, time_obj)

        elif period == 'day' and max_set is True:
            # If there is a new day max, there may be a new month max.
            WeatherData.set_max(metric, 'month', value, time_obj)

        return max_set

    @staticmethod
    def get_min(metric: str, period: str, time_obj: dict, usecache: bool = True):
        """
        Get the minimum value for a given time period.

        :param metric: The metric to get the minimum for, e.g. uv_index
        :param period: The period the minimum relates to. i.e. 'year', 'month', 'day'.
        :param time_obj: The object that contains the time data.
        :param usecache: Use max value from cache. False means get from database.
        :return: The found minimum value.
        """

        min_year = time_obj['year']
        min_month = time_obj['month']
        min_day = time_obj['day']
        tz = pytz.timezone(getattr(settings, 'TIME_ZONE'))

        min_value = {}
        metric_min = '{0}__min'.format(metric)

        # Get value from cache.
        # If cache is empty or invalid get value from the database. Then store in cache.
        if period == 'year':
            cache_key = '_'.join(('min', metric, str(min_year)))
            cache_val = cache.get(cache_key)
            if (cache_val is None) or (usecache is False):
                year_stamp = datetime(min_year, 1, 1, 0, 0, 0, tzinfo=tz).timestamp()
                min_value = WeatherDataModel.objects\
                    .filter(time_year=min_year, time_stamp__gte=year_stamp)\
                    .aggregate(Min(metric))
                if min_value[metric_min] is None:
                    min_value = {metric_min: 0}
            else:
                min_value = {metric_min: cache_val}
        elif period == 'month':
            cache_key = '_'.join(('min', metric, str(min_year), str(min_month)))
            cache_val = cache.get(cache_key)
            if (cache_val is None) or (usecache is False):
                month_stamp = datetime(min_year, min_month, 1, 0, 0, 0, tzinfo=tz).timestamp()
                min_value = WeatherDataModel.objects \
                    .filter(time_year=min_year, time_month=min_month, time_stamp__gte=month_stamp) \
                    .aggregate(Min(metric))
                if min_value[metric_min] is None:
                    min_value = {metric_min: 0}
            else:
                min_value = {metric_min: cache_val}
        elif period == 'day':
            cache_key = '_'.join(('min', metric, str(min_year), str(min_month), str(min_day)))
            cache_val = cache.get(cache_key)
            if (cache_val is None) or (usecache is False):
                day_stamp = datetime(min_year, min_month, min_day, 0, 0, 0, tzinfo=tz).timestamp()
                min_value = WeatherDataModel.objects \
                    .filter(time_year=min_year, time_month=min_month, time_day=min_day, time_stamp__gte=day_stamp) \
                    .aggregate(Min(metric))
                if min_value[metric_min] is None:
                    min_value = {metric_min: 0}
            else:
                min_value = {metric_min: cache_val}
        return min_value

    @staticmethod
    def set_min(metric: str, period: str, value, time_obj: dict) -> bool:
        """
        Set the minimum value for a given time period.
        The value is only "set" in the cache and not updated in the database.
        min values are not stored explicitly in the database but are resolved
        from all stored values.

        :param metric: The metric to get the minimum for, e.g. uv_index
        :param period: The period the minimum relates to. i.e. 'year', 'month', 'day'.
        :param value: The new minimum value.
        :param time_obj: The object that contains the time data.
        :return:
        """

        min_year = time_obj['year']
        min_month = time_obj['month']
        min_day = time_obj['day']
        min_set = False

        # Abort early if metric is not in allowed list
        if metric not in WeatherData.weather_metrics:
            return

        if period == 'year':
            cache_key = '_'.join(('min', metric, str(min_year)))

        elif period == 'month':
            cache_key = '_'.join(('min', metric, str(min_year), str(min_month)))

        elif period == 'day':
            cache_key = '_'.join(('min', metric, str(min_year), str(min_month), str(min_day)))

        cache_val = cache.get(cache_key)  # Raw check of cache.
        if cache_val is None:
            # Cache is empty, get value from database.
            db_val = WeatherData.get_min(metric, period, time_obj, False)
            min_metric = ''.join((metric, '__min'))
            cache_val = db_val.get(min_metric)
            cache.set(cache_key, cache_val, 3600)
            min_set = True

        if cache_val > value:
            cache.set(cache_key, value, 3600)
            min_set = True

        # Do recursive checks if needed.
        if period == 'month' and min_set is True:
            # If there is a new month min, there may also be a new year min.
            # We use recursion (magic) to check.
            WeatherData.set_min(metric, 'year', value, time_obj)

        elif period == 'day' and min_set is True:
            # If there is a new day min, there may be a new month min.
            WeatherData.set_min(metric, 'month', value, time_obj)

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

        # Abort early if metric is not in allowed list
        if metric not in WeatherData.weather_metrics:
            return

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

        # Split out timestamp to date components.
        date_object = datetime.fromtimestamp(timestamp)
        time_obj = {
            'year': date_object.year,
            'month': date_object.month,
            'day': date_object.day

        }

        result_data = {}

        for metric in WeatherData.weather_metrics:
            result_data[metric] = {}
            result_data[metric]['latest'] = WeatherData.get_latest(metric).get('{0}_latest'.format(metric))
            result_data[metric]['daily_max'] = WeatherData.get_max(metric, 'day', time_obj).get('{0}__max'.format(metric))
            result_data[metric]['daily_min'] = WeatherData.get_min(metric, 'day', time_obj).get('{0}__min'.format(metric))
            result_data[metric]['monthly_max'] = WeatherData.get_max(metric, 'month', time_obj).get('{0}__max'.format(metric))
            result_data[metric]['monthly_min'] = WeatherData.get_min(metric, 'month', time_obj).get('{0}__min'.format(metric))
            result_data[metric]['yearly_max'] = WeatherData.get_max(metric, 'year', time_obj).get('{0}__max'.format(metric))
            result_data[metric]['yearly_min'] = WeatherData.get_min(metric, 'year', time_obj).get('{0}__min'.format(metric))

            # Get the trend data.
            if metric in WeatherData.weather_trends:
                # We use slicing here to do some quick and dirty down sampling.
                # Down sampling is based on number of elements (told you it was dirty).
                trend_list = WeatherData.get_trend(metric, 'day', time_obj)
                list_size = len(trend_list)

                if list_size <= 250:
                    result_data[metric]['daily_trend'] = trend_list
                elif (list_size > 250) or (list_size < 100):
                    result_data[metric]['daily_trend'] = UnitConversion.downsample_data(trend_list, 20)
                else:
                    result_data[metric]['daily_trend'] = UnitConversion.downsample_data(trend_list, 60)

        return result_data

    @staticmethod
    def get_trend(metric: str, period: str, time_obj: dict) -> list:
        """
        Get the metric trend data for a given time period.

        :param metric: The metric to get the trend for, e.g. indoor_temp
        :param period: The period the trend relates to. i.e. 'year', 'month', 'day'.
        :param time_obj: The object that contains the time data.
        :return: The trend data.
        """

        trend_year = time_obj['year']
        trend_month = time_obj['month']
        trend_day = time_obj['day']

        trend_data = {}

        # TODO: decide if this needs to be cached.
        if period == 'year':
            trend_data = WeatherDataModel.objects.values_list('time_stamp', metric) \
                .filter(time_year=trend_year) \
                .order_by('time_stamp') \
                .all()
        elif period == 'month':
            trend_data = WeatherDataModel.objects.values_list('time_stamp', metric) \
                .filter(time_year=trend_year, time_month=trend_month) \
                .order_by('time_stamp') \
                .all()
        elif period == 'day':
            trend_data = WeatherDataModel.objects.values_list('time_stamp', metric) \
                .filter(time_year=trend_year, time_month=trend_month, time_day=trend_day) \
                .order_by('time_stamp') \
                .all()

        return list(trend_data)

    @staticmethod
    def get_date_range() -> dict:
        """
        Get the max and min date for the data,
        as well as todays date. All formatted,
        for the date selector.

        :return context: The dict with the date information.
        """

        # Cache max and min values. Min can be cached for ages.
        max_cache_key = 'select_date_max'
        max_cache_val = cache.get(max_cache_key)

        min_cache_key = 'select_date_min'
        min_cache_val = cache.get(min_cache_key)

        if max_cache_val is None:
            max_value = WeatherDataModel.objects.aggregate(Max('time_stamp'))
            maximum = datetime.fromtimestamp(max_value['time_stamp__max']).strftime("%Y-%m-%d")
            cache.set(max_cache_key, maximum, 600)
        else:
            maximum = max_cache_val

        if min_cache_val is None:
            min_value = WeatherDataModel.objects.aggregate(Min('time_stamp'))
            minimum = datetime.fromtimestamp(min_value['time_stamp__min']).strftime("%Y-%m-%d")
            cache.set(min_cache_key, minimum, 86400)
        else:
            minimum = min_cache_val

        today = datetime.now().strftime("%Y-%m-%d")

        context = {
            'minimum': minimum,
            'maximum': maximum,
            'value': today,
        }

        return context
