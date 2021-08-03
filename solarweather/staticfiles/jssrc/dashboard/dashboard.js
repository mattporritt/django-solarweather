// ==============================================================================
//
// This file is part of SolarWeather.
//
// SolarWeather is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// SolarWeather is distributed  WITHOUT ANY WARRANTY:
// without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
// See the GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this software.  If not, see <http://www.gnu.org/licenses/>.
// ==============================================================================

// ==============================================================================
//
// @author Matthew Porritt
// @copyright  2021 onwards Matthew Porritt (mattp@catalyst-au.net)
// @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
// ==============================================================================

'use strict';

import {setup} from './controls.js';

/**
 * Update the dashboard
 *
 * @param {Object} data The raw data to use to update dashboard.
 */
const updateDashboard = (data) => {
    // Individual elements that we will set.
    const indoorTempNow = document.getElementById('indoor-temp-now');
    const indoorTempNowFeelsLike = document.getElementById('indoor-temp-now-feels-like');
    const indoorTempDayMin = document.getElementById('indoor-temp-day-min');
    const indoorTempDayMax = document.getElementById('indoor-temp-day-max');
    const outdoorTempNow = document.getElementById('outdoor-temp-now');
    const outdoorTempNowFeelsLike = document.getElementById('outdoor-temp-now-feels-like');
    const outdoorTempDayMin = document.getElementById('outdoor-temp-day-min');
    const outdoorTempDayMax = document.getElementById('outdoor-temp-day-max');

    // Set the values.
    indoorTempNow.innerHTML = Number.parseFloat(data.indoor_temp.latest).toFixed(1);
    indoorTempNowFeelsLike.innerHTML = Number.parseFloat(data.indoor_feels_temp.latest).toFixed(1);
    indoorTempDayMin.innerHTML = Number.parseFloat(data.indoor_temp.daily_min).toFixed(1);
    indoorTempDayMax.innerHTML = Number.parseFloat(data.indoor_temp.daily_max).toFixed(1);
    outdoorTempNow.innerHTML = Number.parseFloat(data.outdoor_temp.latest).toFixed(1);
    outdoorTempNowFeelsLike.innerHTML = Number.parseFloat(data.outdoor_feels_temp.latest).toFixed(1);
    outdoorTempDayMin.innerHTML = Number.parseFloat(data.outdoor_temp.daily_min).toFixed(1);
    outdoorTempDayMax.innerHTML = Number.parseFloat(data.outdoor_temp.daily_max).toFixed(1);
};

/**
 * Get raw dashboard data.
 *
 * @method getData
 */
const getData = () => {
    fetch('/dataajax/')
        .then((response) => response.json())
        .then((data) => updateDashboard(data));
};

/**
 * Script entry point.
 *
 * @method init
 */
export const init = () => {
    setup(getData);
    getData();
};

