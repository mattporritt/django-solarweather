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

        :param deg_f:
        :param places:
        :return: deg_c
        """

        deg_c = round((deg_f - 32) * (5/9), places)

        return deg_c

    @staticmethod
    def mmhg_to_hpa(mm_hg: float, places: int = 3) -> float:
        """

        :param mm_hg:
        :param places:
        :return: hpa
        """

        hpa = round((mm_hg * 1.33322), places)

        return hpa

    @staticmethod
    def mph_to_kmh(mph: float, places: int = 3) -> float:
        """

        :param mph:
        :param places:
        :return: kmh
        """

        kmh = round((mph * 1.60934), places)

        return kmh

    @staticmethod
    def in_to_cm(inch: float, places: int = 3) -> float:
        """

        :param inch:
        :param places:
        :return: cm
        """

        cm = round((inch * 2.54), places)

        return cm
