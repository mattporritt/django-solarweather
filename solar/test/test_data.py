# ===================t===========================================================
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

test_grid_data = {
   "Body": {
      "Data": {
         "0": {
            "Current_AC_Phase_1": 4.2530000000000001,
            "Current_AC_Sum": 4.2530000000000001,
            "Details": {
               "Manufacturer": "Fronius",
               "Model": "Smart Meter 63A-1",
               "Serial": "17470117"
            },
            "Enable": 1,
            "EnergyReactive_VArAC_Phase_1_Consumed": 8634130,
            "EnergyReactive_VArAC_Phase_1_Produced": 61211500,
            "EnergyReactive_VArAC_Sum_Consumed": 8634130,
            "EnergyReactive_VArAC_Sum_Produced": 61211500,
            "EnergyReal_WAC_Minus_Absolute": 19608086,
            "EnergyReal_WAC_Phase_1_Consumed": 12020406,
            "EnergyReal_WAC_Phase_1_Produced": 19608086,
            "EnergyReal_WAC_Plus_Absolute": 12020406,
            "EnergyReal_WAC_Sum_Consumed": 12020406,
            "EnergyReal_WAC_Sum_Produced": 19608086,
            "Frequency_Phase_Average": 49.899999999999999,
            "Meter_Location_Current": 0,
            "PowerApparent_S_Phase_1": 1046.23,
            "PowerApparent_S_Sum": 1046.23,
            "PowerFactor_Phase_1": 0.93000000000000005,
            "PowerFactor_Sum": 0.93000000000000005,
            "PowerReactive_Q_Phase_1": -325.19,
            "PowerReactive_Q_Sum": -325.19,
            "PowerReal_P_Phase_1": 980.11000000000001,
            "PowerReal_P_Sum": 980.11000000000001,
            "TimeStamp": 1630540304,
            "Visible": 1,
            "Voltage_AC_Phase_1": 246
         }
      }
   },
   "Head": {
      "RequestArguments": {
         "DeviceClass": "Meter",
         "Scope": "System"
      },
      "Status": {
         "Code": 0,
         "Reason": "",
         "UserMessage": ""
      },
      "Timestamp": "2021-09-02T09:51:45+10:00"
   }
}

test_inverter_data = {
   "Body": {
      "Data": {
         "DAY_ENERGY": {
            "Unit": "Wh",
            "Value": 9802
         },
         "DeviceStatus": {
            "ErrorCode": 0,
            "LEDColor": 2,
            "LEDState": 0,
            "MgmtTimerRemainingTime": -1,
            "StateToReset": False,
            "StatusCode": 7
         },
         "FAC": {
            "Unit": "Hz",
            "Value": 49.990000000000002
         },
         "IAC": {
            "Unit": "A",
            "Value": 0.93000000000000005
         },
         "IDC": {
            "Unit": "A",
            "Value": 0.84999999999999998
         },
         "PAC": {
            "Unit": "W",
            "Value": 222
         },
         "TOTAL_ENERGY": {
            "Unit": "Wh",
            "Value": 27236302
         },
         "UAC": {
            "Unit": "V",
            "Value": 242.09999999999999
         },
         "UDC": {
            "Unit": "V",
            "Value": 309.89999999999998
         },
         "YEAR_ENERGY": {
            "Unit": "Wh",
            "Value": 4984010.5
         }
      }
   },
   "Head": {
      "RequestArguments": {
         "DataCollection": "CommonInverterData",
         "DeviceClass": "Inverter",
         "DeviceId": "1",
         "Scope": "Device"
      },
      "Status": {
         "Code": 0,
         "Reason": "",
         "UserMessage": ""
      },
      "Timestamp": "2021-09-03T14:00:05+10:00"
   }
}

test_inverter_data_dark = {
   "Body": {
      "Data": {
         "DAY_ENERGY": {
            "Unit": "Wh",
            "Value": 9802
         },
         "DeviceStatus": {
            "ErrorCode": 0,
            "LEDColor": 2,
            "LEDState": 0,
            "MgmtTimerRemainingTime": -1,
            "StateToReset": False,
            "StatusCode": 7
         },
         "TOTAL_ENERGY": {
            "Unit": "Wh",
            "Value": 27236302
         },
         "YEAR_ENERGY": {
            "Unit": "Wh",
            "Value": 4984010.5
         }
      }
   },
   "Head": {
      "RequestArguments": {
         "DataCollection": "CommonInverterData",
         "DeviceClass": "Inverter",
         "DeviceId": "1",
         "Scope": "Device"
      },
      "Status": {
         "Code": 0,
         "Reason": "",
         "UserMessage": ""
      },
      "Timestamp": "2021-09-03T14:00:05+10:00"
   }
}
