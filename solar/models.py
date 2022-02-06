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


class SolarData(PostgresPartitionedModel):
    """
    This model stores the data received from the solar inverter.
    """
    class PartitioningMeta:
        method = PostgresPartitioningMethod.RANGE
        key = ['time_stamp']

    grid_power_usage_real = models.FloatField()
    grid_power_factor = models.FloatField()
    grid_power_apparent = models.FloatField()
    grid_power_reactive = models.FloatField()
    grid_ac_voltage = models.FloatField()
    grid_ac_current = models.FloatField()
    inverter_ac_frequency = models.FloatField()  # FAC
    inverter_ac_current = models.FloatField()  # IAC
    inverter_ac_voltage = models.FloatField()  # UAC
    inverter_ac_power = models.FloatField()  # PAC
    inverter_dc_current = models.FloatField()  # IDC
    inverter_dc_voltage = models.FloatField()  # UDC
    power_consumption = models.FloatField()
    time_stamp = models.IntegerField(db_index=True)
    time_year = models.IntegerField(db_index=True)
    time_month = models.IntegerField(db_index=True)
    time_day = models.IntegerField(db_index=True)
