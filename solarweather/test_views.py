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

from django.test import TestCase, Client, override_settings
from unittest import mock


# Basic functional testing
class UserFunctionalTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_login(self):

        response = self.client.post('/accounts/login', {'login': user_email,
                                                        'password': user_passsword,
                                                        'next': '/'}
                                    )
        # Response code should be a redirect if login successful
        # and content should be empty
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'')
