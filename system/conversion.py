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

class UnitConversion:
    """
    Helper class that provides methods to convert between units.
    """

    @staticmethod
    def f_to_c(deg_f: float, places: int = 3) -> float:
        """
        Convert fahrenheit to celsius to an optional number
        of places.

        :param deg_f: The temp in degrees fahrenheit to convert from.
        :param places: The number of decimal places to return in the converted result.
        :return: deg_c: The converted temp in degrees celsius.
        """

        deg_c = round((deg_f - 32) * (5/9), places)

        return deg_c

    @staticmethod
    def inhg_to_hpa(inch_hg: float, places: int = 3) -> float:
        """
        Convert pressure in inches of mercury to hectopascals.

        :param inch_hg: The pressure in inches of mercury to convert from.
        :param places: The number of decimal places to return in the converted result.
        :return: hpa: The converted pressure in hectopascals.
        """

        hpa = round((inch_hg * 33.86389), places)

        return hpa

    @staticmethod
    def mph_to_kmh(mph: float, places: int = 3) -> float:
        """
        Convert speed in miles per hour to kilometers per hour.

        :param mph: The speed in miles per hour to convert from.
        :param places: The number of decimal places to return in the converted result.
        :return: kmh: The converted speed in kilometers per hour.
        """

        kmh = round((mph * 1.60934), places)

        return kmh

    @staticmethod
    def in_to_cm(inch: float, places: int = 3) -> float:
        """
        Convert length/depth in inches to centimeters.

        :param inch: The length/depth in inches to convert from.
        :param places: The number of decimal places to return in the converted result.
        :return: cm: The converted length/depth in centimeters.
        """

        cm = round((inch * 2.54), places)

        return cm
