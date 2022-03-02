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

import requests
from django.conf import settings
from datetime import datetime, timedelta
from solar.models import SolarData as SolarDataModel
from weather.weatherdata import WeatherData
from system.conversion import UnitConversion
from django.core.cache import cache

import logging

# Get an instance of a logger
logger = logging.getLogger('django')

class SolarData:
    """
    Class to get inverter data and related operations.
    """

    # Metrics we can query and get data for.
    solar_metrics = [
        'grid_power_usage_real',
        'inverter_ac_power',
        'power_consumption',
    ]

    # Metrics to get accumulated data for.
    accumulated_metrics = [
        'inverter_ac_power',
        'power_consumption',
    ]

    # Metrics to get trend data for.
    solar_trends = [
        'grid_power_usage_real',
        'inverter_ac_power',
    ]

    @staticmethod
    def get_date_obj(timestamp: int) -> dict:
        """
        Custom processing to convert a timestamp into components
        used in various processing.

        :param timestamp: The unix timestamp to get the date object for.
        :return time_obj: The date object
        """

        # Split out timestamp to date components.
        date_object = datetime.fromtimestamp(timestamp)

        start = date_object - timedelta(days=(date_object.weekday() + 1) % 7)
        end = start + timedelta(days=6)

        time_obj = {
            'year': date_object.year,
            'month': date_object.month,
            'week': date_object.isocalendar()[1],
            'day': date_object.day,
            'week_start_day': start.day,
            'week_end_day': end.day
        }

        return time_obj

    @staticmethod
    def get_grid_data() -> dict:
        """
        Query the Fronius inverter for grid power data.

        :return grid_data: The grid data received from the inverter.
        """

        inverter_domain = getattr(settings, 'SOLAR_API')
        inverter_uri = 'http://{0}/solar_api/v1/GetMeterRealtimeData.cgi'.format(inverter_domain)
        query_params = {'Scope': 'System'}
        request_response = requests.get(inverter_uri, params=query_params)
        grid_data_raw = request_response.json()['Body']['Data']['0']

        # Just grab the data we want.
        grid_data = {
            'grid_power_usage_real': grid_data_raw.get('PowerReal_P_Sum', 0),
            'grid_power_factor': grid_data_raw.get('PowerFactor_Sum', 0),
            'grid_power_apparent': grid_data_raw.get('PowerApparent_S_Sum', 0),
            'grid_power_reactive': grid_data_raw.get('PowerReactive_Q_Sum', 0),
            'grid_ac_voltage': grid_data_raw.get('Voltage_AC_Phase_1', 0),
            'grid_ac_current': grid_data_raw.get('Current_AC_Sum', 0)
        }

        return grid_data

    @staticmethod
    def get_inverter_data() -> dict:
        """
        Query the Fronius inverter for inverter and solar power data.

        :return inverter_data: The solar data received from the inverter.
        """

        inverter_domain = getattr(settings, 'SOLAR_API')
        inverter_uri = 'http://{0}/solar_api/v1/GetInverterRealtimeData.cgi'.format(inverter_domain)
        query_params = {'Scope': 'Device', 'DeviceId': '1', 'DataCollection': 'CommonInverterData'}
        request_response = requests.get(inverter_uri, params=query_params)
        inverter_data_raw = request_response.json()['Body']['Data']

        # Just grab the data we want.
        inverter_data = {
            'inverter_ac_frequency': inverter_data_raw.get('FAC', {'Unit': 'Hz', 'Value': 0})['Value'],
            'inverter_ac_current': inverter_data_raw.get('IAC', {'Unit': 'A', 'Value': 0})['Value'],
            'inverter_ac_voltage': inverter_data_raw.get('UAC', {'Unit': 'V', 'Value': 0})['Value'],
            'inverter_ac_power': inverter_data_raw.get('PAC', {'Unit': 'W', 'Value': 0})['Value'],
            'inverter_dc_current': inverter_data_raw.get('IDC', {'Unit': 'A', 'Value': 0})['Value'],
            'inverter_dc_voltage': inverter_data_raw.get('UDC', {'Unit': 'V', 'Value': 0})['Value']
        }

        return inverter_data

    @staticmethod
    def get_inst_power_consumption(inverter_power: float, grid_power: float) -> float:
        """
        Calculate the power consumption of the house,
        based on the difference between the inverter and
        grid power.

        :param inverter_power: The power from the inverter always positive.
        :param grid_power: The power from the grid positive or negative.
        :return power_consumption: The power consumption of the house.
        """

        # Power consumption for the house is always above zero (positive).
        # The power from the inverter is always zero or above (positive).
        # The power from the grid can be either positive or negative.
        # The power from the inverter is always used by the house first.

        if grid_power <= 0:
            power_diff = inverter_power - abs(grid_power)
            power_consumption = abs(power_diff)
        else:
            power_consumption = inverter_power + grid_power

        return power_consumption

    @staticmethod
    def get_latest(metric: str) -> dict:
        """
        Get the latest received value for a metric

        :param: metric: The metric to get the latest for, e.g. uv_index
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
    def get_accumulated_area(data_table: list, magnitude_field: str, time_field: str) -> float:
        """
        Take a table of time based data and return the accumulated area under the curve.
        Useful for taking instantaneous power readings and using them to calculate,
        the power consumption over time.

        The output will be per hour.

        :param data_table: The table containing the raw data pairs.
        :param magnitude_field: The key value for the magnitude data.
        :param time_field: The key value for the time data.
        :return accumulated_area: The accumulated are per hour.
        """

        row_count = 0
        accumulated_area = 0
        for data_row in data_table:
            if row_count > 0:
                current_time = data_row[time_field]
                previous_time = data_table[(row_count - 1)][time_field]
                current_magnitude = data_row[magnitude_field]
                previous_magnitude = data_table[(row_count - 1)][magnitude_field]
                time_period = (current_time - previous_time) / 3600

                # Calculate the "main" rectangle under the curve and add it to the area total.
                accumulated_area += current_magnitude * time_period

                # Next add the "triangle" at the top of rectangle.
                accumulated_area += (current_magnitude - previous_magnitude) * time_period * 0.5

            row_count += 1

        return accumulated_area

    @staticmethod
    def get_accumulated(metric: str, period: str, time_obj: dict, usecache: bool = True) -> float:
        """
        Get the accumulated value for a metric for the given period (day, month, week, or year).
        By accumulated we mean the area under the curve. For example the total power generated for a day.
        If the value is not cached it is calculated and then the value is set in the cache

        :param metric: The metric to get the daily value for, e.g. uv_index
        :param period: The period the maximum relates to. i.e. 'year', 'month', 'day'.
        :param time_obj: The object that contains the time data.
        :param usecache: Use max value from cache. False means get from database.
        :return: The accumulated value.
        """

        accum_value = 0

        # Get value from cache.
        # If cache is empty or invalid get value from the database. Then store in cache.
        if period == 'year':
            cache_key = '_'.join(('accum', metric, str(time_obj['year'])))
            cache_val = cache.get(cache_key)
            if (cache_val is None) or (usecache is False):
                accum_objects = SolarDataModel.objects\
                    .filter(time_year=time_obj['year']) \
                    .values('time_stamp', metric) \
                    .order_by('time_stamp')
                accum_value = SolarData.get_accumulated_area(accum_objects, metric, 'time_stamp')
                cache.set(cache_key, accum_value, 3600)
            else:
                accum_value = cache_val
        elif period == 'month':
            cache_key = '_'.join(('accum', metric, str(time_obj['year']), str(time_obj['month'])))
            cache_val = cache.get(cache_key)
            if (cache_val is None) or (usecache is False):
                accum_objects = SolarDataModel.objects \
                    .filter(time_year=time_obj['year'], time_month=time_obj['month']) \
                    .values('time_stamp', metric)\
                    .order_by('time_stamp')
                accum_value = SolarData.get_accumulated_area(accum_objects, metric, 'time_stamp')
                cache.set(cache_key, accum_value, 3600)
            else:
                accum_value = cache_val
        elif period == 'week':
            cache_key = '_'.join(('accum', metric, str(time_obj['year']), str(time_obj['week'])))
            cache_val = cache.get(cache_key)
            if (cache_val is None) or (usecache is False):
                accum_objects = SolarDataModel.objects \
                    .filter(time_year=time_obj['year'], time_month=time_obj['month'],
                            time_day__gte=time_obj['week_start_day'], time_day__lte=time_obj['week_end_day']) \
                    .values('time_stamp', metric) \
                    .order_by('time_stamp')
                accum_value = SolarData.get_accumulated_area(accum_objects, metric, 'time_stamp')
                cache.set(cache_key, accum_value, 1800)
            else:
                accum_value = cache_val
        elif period == 'day':
            cache_key = '_'.join(('accum', metric, str(time_obj['year']), str(time_obj['month']), str(time_obj['day'])))
            cache_val = cache.get(cache_key)
            if (cache_val is None) or (usecache is False):
                accum_objects = SolarDataModel.objects \
                    .filter(time_year=time_obj['year'], time_month=time_obj['month'], time_day=time_obj['day']) \
                    .values('time_stamp', metric) \
                    .order_by('time_stamp')
                accum_value = SolarData.get_accumulated_area(accum_objects, metric, 'time_stamp')
                cache.set(cache_key, accum_value, 600)
            else:
                accum_value = cache_val

        return accum_value

    @staticmethod
    def store(timestamp: int = 0) -> int:
        """
        Store received weather station data into database.

        :param timestamp: Time data was received.
        :return: ID of inserted row.
        """

        # If timestamp is not provided default to now.
        if timestamp == 0:
            timestamp = datetime.now().timestamp()

        date_object = datetime.fromtimestamp(timestamp)

        # Get the raw data.
        grid_data = SolarData.get_grid_data()
        inverter_data = SolarData.get_inverter_data()

        # Do some calculations.
        power_consumption = SolarData.get_inst_power_consumption(
            inverter_data['inverter_ac_power'], grid_data['grid_power_usage_real'])

        # Prepare data object to be stored in database.
        store_data = {
            'grid_power_usage_real': grid_data['grid_power_usage_real'],
            'grid_power_factor': grid_data['grid_power_factor'],
            'grid_power_apparent': grid_data['grid_power_apparent'],
            'grid_power_reactive': grid_data['grid_power_reactive'],
            'grid_ac_voltage': grid_data['grid_ac_voltage'],
            'grid_ac_current': grid_data['grid_ac_current'],
            'inverter_ac_frequency': inverter_data['inverter_ac_frequency'],
            'inverter_ac_current': inverter_data['inverter_ac_current'],
            'inverter_ac_voltage': inverter_data['inverter_ac_voltage'],
            'inverter_ac_power': inverter_data['inverter_ac_power'],
            'inverter_dc_current': inverter_data['inverter_dc_current'],
            'inverter_dc_voltage': inverter_data['inverter_dc_voltage'],
            'power_consumption': power_consumption,
            'time_stamp': timestamp,
            'time_year': date_object.year,
            'time_month': date_object.month,
            'time_day': date_object.day
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
                # SolarData.set_max(metric, 'day', value, time_obj)
                # SolarData.set_min(metric, 'day', value, time_obj)
                SolarData.set_latest(metric, value)

        # Store data in the database.
        data_record = SolarDataModel(**store_data)
        data_record.save()

        # Return ID of inserted row.
        return data_record.id

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
            SolarDataModel.name
            trend_data = SolarDataModel.objects.values_list('time_stamp', metric) \
                .filter(time_year=trend_year) \
                .order_by('time_stamp') \
                .all()
        elif period == 'month':
            trend_data = SolarDataModel.objects.values_list('time_stamp', metric) \
                .filter(time_year=trend_year, time_month=trend_month) \
                .order_by('time_stamp') \
                .all()
        elif period == 'day':
            trend_data = SolarDataModel.objects.values_list('time_stamp', metric) \
                .filter(time_year=trend_year, time_month=trend_month, time_day=trend_day) \
                .order_by('time_stamp') \
                .all()

        return list(trend_data)

    @staticmethod
    def get_data(timestamp: int = 0) -> dict:
        """
        Get all the data to display the solar dashboard.
        Data returned:
            Current power usage for the house in kWh
            Current power draw from the solar panels in kWh.
            Current power draw from the grid in kWh

        :param timestamp:
        :return:
        """

        # If timestamp is not provided default to now.
        if timestamp == 0:
            timestamp = datetime.now().timestamp()

        # Split out timestamp to date components.
        date_object = SolarData.get_date_obj(timestamp)

        result_data = {}

        for metric in SolarData.solar_metrics:
            result_data[metric] = {}
            result_data[metric]['latest'] = SolarData.get_latest(metric).get('{0}_latest'.format(metric))

            if metric in SolarData.accumulated_metrics:
                result_data[metric]['day'] = SolarData.get_accumulated(metric, 'day', date_object)
                result_data[metric]['week'] = SolarData.get_accumulated(metric, 'week', date_object)
                result_data[metric]['month'] = SolarData.get_accumulated(metric, 'month', date_object)

            # Get the trend data.
            if metric in SolarData.solar_trends:
                # We use slicing here to do some quick and dirty down sampling.
                # Down sampling is based on number of elements (told you it was dirty).
                trend_list = SolarData.get_trend(metric, 'day', date_object)
                list_size = len(trend_list)

                if list_size <= 250:
                    result_data[metric]['daily_trend'] = trend_list
                elif (list_size > 250) or (list_size < 100):
                    result_data[metric]['daily_trend'] = UnitConversion.downsample_data(trend_list, 50)
                else:
                    result_data[metric]['daily_trend'] = UnitConversion.downsample_data(trend_list, 100)

        # Get some solar related data from the weather station.
        result_data['solar_radiation'] = {}
        result_data['uv_index'] = {}
        result_data['solar_radiation']['latest'] = WeatherData.get_latest('solar_radiation').get('{0}_latest'.format('solar_radiation'))
        result_data['uv_index']['latest'] = WeatherData.get_latest('uv_index').get('{0}_latest'.format('uv_index'))

        return result_data

    @staticmethod
    def get_date_range() -> dict:
        """
        Get the max and min date for the data,
        as well as todays date. All formatted,
        for the date selector.

        :return context: The dict with the date information.
        """

        # TODO: cache max and min values. Min can be cached for ages.

        context = {
            'min': '2021-01-01',
            'max': '2022-03-05',
            'value': '2022-03-02',
        }

        return context
