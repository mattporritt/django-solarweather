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

from django.test import TestCase
from system.conversion import UnitConversion
import system.test.test_data as test_data

import logging

# Get an instance of a logger
logger = logging.getLogger('django')

# Basic functional testing
class ConversionUnitTestCase(TestCase):

    def test_f_to_c_zero_c(self):
        """
        Test converting to zero degrees celsius,
        also not setting an explicit number or decimal places.
        """
        deg_c = UnitConversion.f_to_c(32)

        self.assertEqual(deg_c, 0)

    def test_f_to_c_hundred_f(self):
        """
        Test converting from 100 degrees F,
        also not setting an explicit number or decimal places.
        """
        deg_c = UnitConversion.f_to_c(100)

        self.assertEqual(deg_c, 37.778)

    def test_f_to_c_two_decimal(self):
        """
        Test converting from 100 degrees F,
        also setting 2 decimal places.
        """
        deg_c = UnitConversion.f_to_c(100, 2)

        self.assertEqual(deg_c, 37.78)

    def test_f_to_c_four_decimal(self):
        """
        Test converting to zero degrees celsius,
        also setting 2 decimal places.
        """
        deg_c = UnitConversion.f_to_c(100, 4)

        self.assertEqual(deg_c, 37.7778)

    def test_inhg_to_hpa(self):
        """
        Test converting inches of mercury to hectopascals,
        also not setting an explicit number or decimal places.
        """
        hpa = UnitConversion.inhg_to_hpa(29.714)

        self.assertEqual(hpa, 1006.232)

    def test_mph_to_kmh(self):
        """
        Test converting miles per hour to kilometers per hour,
        also not setting an explicit number or decimal places.
        """
        kmh = UnitConversion.mph_to_kmh(100)

        self.assertEqual(kmh, 160.934)

    def test_in_to_cm(self):
        """
        Test inches to centimeters,
        also not setting an explicit number or decimal places.
        """
        cm = UnitConversion.in_to_cm(100)

        self.assertEqual(cm, 254)

    def test_downsample_data(self):
        """
        Test down sampling.
        """
        sample_size = 10
        result_list = UnitConversion.downsample_data(test_data.test_trend_list, sample_size)

        self.assertEqual(result_list[0][0], 1631855251)
        self.assertEqual(result_list[0][1], -3677.407)
