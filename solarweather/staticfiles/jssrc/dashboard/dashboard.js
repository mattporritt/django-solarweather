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
 * @param {Object} Chart The chart object.
 */
let Chart;

/**
 * Render the graph.
 *
 * @param {String} canvasId The ID of the canvas HTML element.
 */
const renderGraph = (canvasId) => {
    const labels = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
    ];
    const data = {
        labels: labels,
        datasets: [{
            label: 'My First dataset',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [0, 10, 5, 2, 20, 30, 45],
        }],
    };
    const config = {
        type: 'line',
        data: data,
    };

    const foo = new Chart(
        document.getElementById(canvasId),
        config
    );
    window.console.log(foo);
};

/**
 * Update the dashboard
 *
 * @param {Object} data The raw data to use to update dashboard.
 */
const updateDashboard = (data) => {
    // Parent card elements.
    const indoorTempCard = document.getElementById('dashboard-indoor-temp-card');
    const indoorTempSpinner = indoorTempCard.querySelector('.loading-spinner');
    const indoorTempOverlay = indoorTempCard.querySelector('.overlay');
    const indoorTempBlur = indoorTempCard.querySelectorAll('.blur');

    // Individual elements that we will set.
    const indoorTempNow = document.getElementById('indoor-temp-now');
    const indoorTempNowFeelsLike = document.getElementById('indoor-temp-now-feels-like');
    const indoorTempDayMin = document.getElementById('indoor-temp-day-min');
    const indoorTempDayMax = document.getElementById('indoor-temp-day-max');
    const outdoorTempNow = document.getElementById('outdoor-temp-now');
    const outdoorTempNowFeelsLike = document.getElementById('outdoor-temp-now-feels-like');
    const outdoorTempDayMin = document.getElementById('outdoor-temp-day-min');
    const outdoorTempDayMax = document.getElementById('outdoor-temp-day-max');

    // Handle some potential null conditions.
    const indoorTempNowVal = data.indoor_temp.latest ? data.indoor_temp.latest : 0;
    const indoorTempNowFeelsLikeVal = data.indoor_feels_temp.latest? data.indoor_temp.latest : 0;
    const outdoorTempNowVal = data.outdoor_temp.latest ? data.outdoor_temp.latest : 0;
    const outdoorTempNowFeelsLikeVal = data.outdoor_feels_temp.latest ? data.outdoor_feels_temp.latest : 0;

    // Set the values.
    indoorTempNow.innerHTML = Number.parseFloat(indoorTempNowVal).toFixed(1);
    indoorTempNowFeelsLike.innerHTML = Number.parseFloat(indoorTempNowFeelsLikeVal).toFixed(1);
    indoorTempDayMin.innerHTML = Number.parseFloat(data.indoor_temp.daily_min).toFixed(1);
    indoorTempDayMax.innerHTML = Number.parseFloat(data.indoor_temp.daily_max).toFixed(1);
    outdoorTempNow.innerHTML = Number.parseFloat(outdoorTempNowVal).toFixed(1);
    outdoorTempNowFeelsLike.innerHTML = Number.parseFloat(outdoorTempNowFeelsLikeVal).toFixed(1);
    outdoorTempDayMin.innerHTML = Number.parseFloat(data.outdoor_temp.daily_min).toFixed(1);
    outdoorTempDayMax.innerHTML = Number.parseFloat(data.outdoor_temp.daily_max).toFixed(1);

    // Render the graphs.
    renderGraph('indoor-temp-chart');

    // Remove the blur effect etc.
    indoorTempSpinner.style.display = 'none';
    indoorTempOverlay.style.display = 'none';
    indoorTempBlur.forEach((BlurredItem) =>{
        BlurredItem.classList.remove('blur');
    });
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
 * @param {Object} chart The chart object.
 *
 */
export const init = (chart) => {
    Chart = chart;
    setup(getData);
    getData();
};

