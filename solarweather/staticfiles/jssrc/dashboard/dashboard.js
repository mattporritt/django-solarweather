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
 * This class allows setting up the configuration object
 * that is used in charts.
 *
 * @class WeatherChartConfig
 */
class WeatherChartConfig {
    /**
     * Constructor method for the class.
     */
    constructor() {
        this.config = {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    backgroundColor: '#c68200',
                    borderColor: '#FF8C00',
                    data: [],
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false,
                    },
                },
                scales: {
                    x: {
                        grid: {
                            color: 'rgb(255, 255, 255, 0.5)',
                        },
                        ticks: {
                            color: 'rgb(255, 255, 255)',
                        },
                    },
                    y: {
                        grid: {
                            color: 'rgb(255, 255, 255, 0.5)',
                        },
                        ticks: {
                            color: 'rgb(255, 255, 255)',
                        },
                    },
                },
            },
        };
    }
}

/**
 * @param {Object} Chart The chart object factory.
 */
let Chart;

/**
 * @param {Object} weatherCharts The charts to make.
 */
const weatherCharts = {
    'indoorTemp': {'id': 'indoor-temp-chart', 'chartObj': null, 'dataLabel': 'indoor_temp'},
    'outdoorTemp': {'id': 'outdoor-temp-chart', 'chartObj': null, 'dataLabel': 'outdoor_temp'},
};

/**
 * Update the graphs.
 *
 * @param {String} chartName The chart to update.
 * @param {Object} updateData The data to update the charts with.
 */
const updateGraphs = (chartName, updateData) => {
    weatherCharts[chartName].chartObj.data.labels = updateData.labels;
    weatherCharts[chartName].chartObj.data.datasets[0].data = updateData.values;
    weatherCharts[chartName].chartObj.update();
};

/**
 * Format the timestamps given in the trend data into readable times.
 *
 *  @param {Object} data The data to update the charts with.
 *  @return {Promise} The data processed.
 */
const formatDate = (data) => {
    const labelDates = [];
    return new Promise((resolve, reject) => {
        data.labels.forEach((label) =>{
            const dateObj = new Date(label * 1000);
            const hours = dateObj.getHours();
            const minutes = '0' + dateObj.getMinutes();
            const strftimetime = hours + ':' + minutes.substr(-2); // Will display time in 10:30 format.
            labelDates.push(strftimetime);
        });
        resolve({'labels': labelDates, 'values': data.values});
    });
};

/**
 * Format the trend data ready for the charts.
 *
 * @param {Object} data The data to update the charts with.
 * @return {Promise} The data processed.
 */
const formatTrend = (data) => {
    const labels = [];
    const values = [];
    return new Promise((resolve, reject) => {
        data.forEach((datapair) =>{
            labels.push(datapair[0]);
            values.push(datapair[1]);
        });
        resolve({'labels': labels, 'values': values});
    });
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

    const outdoorTempCard = document.getElementById('dashboard-outdoor-temp-card');
    const outdoorTempSpinner = outdoorTempCard.querySelector('.loading-spinner');
    const outdoorTempOverlay = outdoorTempCard.querySelector('.overlay');
    const outdoorTempBlur = outdoorTempCard.querySelectorAll('.blur');

    const humidityCard = document.getElementById('dashboard-humidity-card');
    const humiditySpinner = humidityCard.querySelector('.loading-spinner');
    const humidityOverlay = humidityCard.querySelector('.overlay');
    const humidityBlur = humidityCard.querySelectorAll('.blur');

    const rainCard = document.getElementById('dashboard-rain-card');
    const rainSpinner = rainCard.querySelector('.loading-spinner');
    const rainOverlay = rainCard.querySelector('.overlay');
    const rainBlur = rainCard.querySelectorAll('.blur');

    const pressureCard = document.getElementById('dashboard-pressure-card');
    const pressureSpinner = pressureCard.querySelector('.loading-spinner');
    const pressureOverlay = pressureCard.querySelector('.overlay');
    const pressureBlur = pressureCard.querySelectorAll('.blur');

    // Individual elements that we will set.
    const indoorTempNow = document.getElementById('indoor-temp-now');
    const indoorTempNowFeelsLike = document.getElementById('indoor-temp-now-feels-like');
    const indoorTempDayMin = document.getElementById('indoor-temp-day-min');
    const indoorTempDayMax = document.getElementById('indoor-temp-day-max');

    const outdoorTempNow = document.getElementById('outdoor-temp-now');
    const outdoorTempNowFeelsLike = document.getElementById('outdoor-temp-now-feels-like');
    const outdoorTempDayMin = document.getElementById('outdoor-temp-day-min');
    const outdoorTempDayMax = document.getElementById('outdoor-temp-day-max');

    const indoorHumidityNow = document.getElementById('indoor-humidity-now');
    const indoorHumidityDayMin = document.getElementById('indoor-humidity-day-min');
    const indoorHumidityDayMax = document.getElementById('indoor-humidity-day-max');
    const outdoorHumidityNow = document.getElementById('outdoor-humidity-now');
    const outdoorHumidityDayMin = document.getElementById('outdoor-humidity-day-min');
    const outdoorHumidityDayMax = document.getElementById('outdoor-humidity-day-max');

    const rainDay = document.getElementById('rain-day');
    const rainRate = document.getElementById('rain-rate');
    const rainWeek = document.getElementById('rain-week');
    const rainMonth = document.getElementById('rain-month');

    const pressureNow = document.getElementById('pressure-now');
    const pressureDayMin = document.getElementById('pressure-day-min');
    const pressureDayMax = document.getElementById('pressure-day-max');

    // Handle some potential null conditions.
    const indoorTempNowVal = data.indoor_temp.latest ? data.indoor_temp.latest : 0;
    const indoorTempNowFeelsLikeVal = data.indoor_feels_temp.latest? data.indoor_feels_temp.latest : 0;

    const outdoorTempNowVal = data.outdoor_temp.latest ? data.outdoor_temp.latest : 0;
    const outdoorTempNowFeelsLikeVal = data.outdoor_feels_temp.latest ? data.outdoor_feels_temp.latest : 0;

    const indoorHumidityNowVal = data.indoor_humidity.latest ? data.indoor_humidity.latest : 0;
    const outdoorHumidityNowVal = data.outdoor_humidity.latest ? data.outdoor_humidity.latest : 0;

    // Calculations.
    const nowDate = new Date();
    const nowHours = nowDate.getHours() + 1;
    const rainRateVal = data.daily_rain.latest / nowHours;

    // Set the values.
    indoorTempNow.innerHTML = Number.parseFloat(indoorTempNowVal).toFixed(1);
    indoorTempNowFeelsLike.innerHTML = Number.parseFloat(indoorTempNowFeelsLikeVal).toFixed(1);
    indoorTempDayMin.innerHTML = Number.parseFloat(data.indoor_temp.daily_min).toFixed(1);
    indoorTempDayMax.innerHTML = Number.parseFloat(data.indoor_temp.daily_max).toFixed(1);

    outdoorTempNow.innerHTML = Number.parseFloat(outdoorTempNowVal).toFixed(1);
    outdoorTempNowFeelsLike.innerHTML = Number.parseFloat(outdoorTempNowFeelsLikeVal).toFixed(1);
    outdoorTempDayMin.innerHTML = Number.parseFloat(data.outdoor_temp.daily_min).toFixed(1);
    outdoorTempDayMax.innerHTML = Number.parseFloat(data.outdoor_temp.daily_max).toFixed(1);

    indoorHumidityNow.innerHTML = Number.parseInt(indoorHumidityNowVal);
    indoorHumidityDayMin.innerHTML = Number.parseInt(data.indoor_humidity.daily_min);
    indoorHumidityDayMax.innerHTML = Number.parseInt(data.indoor_humidity.daily_max);

    outdoorHumidityNow.innerHTML = Number.parseInt(outdoorHumidityNowVal);
    outdoorHumidityDayMin.innerHTML = Number.parseInt(data.outdoor_humidity.daily_min);
    outdoorHumidityDayMax.innerHTML = Number.parseInt(data.outdoor_humidity.daily_max);

    rainDay.innerHTML = Number.parseFloat(data.daily_rain.latest).toFixed(1);
    rainRate.innerHTML = Number.parseFloat(rainRateVal).toFixed(1);
    rainWeek.innerHTML = Number.parseFloat(data.weekly_rain.latest).toFixed(1);
    rainMonth.innerHTML = Number.parseFloat(data.monthly_rain.latest).toFixed(1);

    pressureNow.innerHTML = Number.parseFloat(data.pressure.latest).toFixed(2);
    pressureDayMin.innerHTML = Number.parseFloat(data.pressure.daily_min).toFixed(2);
    pressureDayMax.innerHTML = Number.parseFloat(data.pressure.daily_max).toFixed(2);

    // Update the charts.
    for (const chartName in weatherCharts) {
        if ({}.hasOwnProperty.call(weatherCharts, chartName)) {
            const trendName = weatherCharts[chartName].dataLabel;
            formatTrend(data[trendName].daily_trend)
                .then(formatDate)
                .then((trendData) => {
                    updateGraphs(chartName, trendData);
                });
        }
    }

    // Remove the blur effect etc.
    indoorTempSpinner.style.display = 'none';
    indoorTempOverlay.style.display = 'none';
    indoorTempBlur.forEach((BlurredItem) =>{
        BlurredItem.classList.remove('blur');
    });

    outdoorTempSpinner.style.display = 'none';
    outdoorTempOverlay.style.display = 'none';
    outdoorTempBlur.forEach((BlurredItem) =>{
        BlurredItem.classList.remove('blur');
    });

    humiditySpinner.style.display = 'none';
    humidityOverlay.style.display = 'none';
    humidityBlur.forEach((BlurredItem) =>{
        BlurredItem.classList.remove('blur');
    });

    rainSpinner.style.display = 'none';
    rainOverlay.style.display = 'none';
    rainBlur.forEach((BlurredItem) =>{
        BlurredItem.classList.remove('blur');
    });

    pressureSpinner.style.display = 'none';
    pressureOverlay.style.display = 'none';
    pressureBlur.forEach((BlurredItem) =>{
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
    const chartConfigObj = new WeatherChartConfig();

    // Setup the initial charts.
    for (const chartName in weatherCharts) {
        if ({}.hasOwnProperty.call(weatherCharts, chartName)) {
            weatherCharts[chartName].chartObj = new Chart(
                document.getElementById(weatherCharts[chartName].id),
                chartConfigObj.config
            );
        }
    }

    // Setup auto retrieving of data.
    setup(getData);

    // Get initial data to kick things off.
    getData();
};

