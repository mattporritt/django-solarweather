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
    // Parent card elements.
    const currentUsageCard = document.getElementById('dashboard-current-usage-card');
    const currentUsageSpinner = currentUsageCard.querySelector('.loading-spinner');
    const currentUsageOverlay = currentUsageCard.querySelector('.overlay');
    const currentUsageBlur = currentUsageCard.querySelectorAll('.blur');

    const dailyPowerCard = document.getElementById('dashboard-daily-power-card');
    const dailyPowerSpinner = dailyPowerCard.querySelector('.loading-spinner');
    const dailyPowerOverlay = dailyPowerCard.querySelector('.overlay');
    const dailyPowerBlur = dailyPowerCard.querySelectorAll('.blur');

    const lightCard = document.getElementById('dashboard-light-card');
    const lightSpinner = lightCard.querySelector('.loading-spinner');
    const lightOverlay = lightCard.querySelector('.overlay');
    const lightBlur = lightCard.querySelectorAll('.blur');

    // Individual elements that we will set.
    const currentUsageNow = document.getElementById('current-usage-now');
    const currentUsageFromSolar = document.getElementById('current-usage-from-solar');
    const currentUsageFromGrid = document.getElementById('current-usage-from-grid');

    const generatedDay = document.getElementById('generated-day');
    const generatedWeek = document.getElementById('generated-week');
    const generatedMonth = document.getElementById('generated-month');
    const usedDay = document.getElementById('used-day');
    const usedWeek = document.getElementById('used-week');
    const usedMonth = document.getElementById('used-month');

    const currentUvIndex = document.getElementById('uv-index');
    const currentLightIntensity = document.getElementById('light-intensity');

    // Handle some potential null conditions.
    const currentUsageNowVal = data.power_consumption.latest ? data.power_consumption.latest : 0;
    const currentUsageFromSolarVal = data.inverter_ac_power.latest? data.inverter_ac_power.latest : 0;
    const currentUsageFromGridVal = data.grid_power_usage_real.latest? data.grid_power_usage_real.latest : 0;

    const generatedDayVal = data.inverter_ac_power.day ? data.inverter_ac_power.day : 0;
    const generatedWeekVal = data.inverter_ac_power.week ? data.inverter_ac_power.week : 0;
    const generatedMonthVal = data.inverter_ac_power.month ? data.inverter_ac_power.month : 0;
    const usedDayVal = data.power_consumption.day ? data.power_consumption.day : 0;
    const usedWeekVal = data.power_consumption.week ? data.power_consumption.week : 0;
    const usedMonthVal = data.power_consumption.month ? data.power_consumption.month : 0;

    const currentUvIndexVal = data.uv_index.latest ? data.uv_index.latest : 0;
    const ccurrentLightIntensityVal = data.solar_radiation.latest? data.solar_radiation.latest : 0;

    // Calculations.
    const currentUsageNowValFloat = Number.parseFloat(currentUsageNowVal) / 1000;
    const currentUsageFromSolarValFloat = Number.parseFloat(currentUsageFromSolarVal) / 1000;
    const currentUsageFromGridValFloat = Number.parseFloat(currentUsageFromGridVal) / 1000;

    const generatedDayValFloat = Number.parseFloat(generatedDayVal) / 1000;
    const generatedWeekValFloat = Number.parseFloat(generatedWeekVal) / 1000;
    const generatedMonthValFloat = Number.parseFloat(generatedMonthVal) / 1000;
    const usedDayValFloat = Number.parseFloat(usedDayVal) / 1000;
    const usedWeekValFloat = Number.parseFloat(usedWeekVal) / 1000;
    const usedMonthValFloat = Number.parseFloat(usedMonthVal) / 1000;

    // Set the values.
    currentUsageNow.innerHTML = currentUsageNowValFloat.toFixed(3);
    currentUsageFromSolar.innerHTML = currentUsageFromSolarValFloat.toFixed(3);
    currentUsageFromGrid.innerHTML = currentUsageFromGridValFloat.toFixed(3);

    generatedDay.innerHTML = generatedDayValFloat.toFixed(3);
    generatedWeek.innerHTML = generatedWeekValFloat.toFixed(1);
    generatedMonth.innerHTML = generatedMonthValFloat.toFixed(1);
    usedDay.innerHTML = usedDayValFloat.toFixed(3);
    usedWeek.innerHTML = usedWeekValFloat.toFixed(1);
    usedMonth.innerHTML = usedMonthValFloat.toFixed(1);

    currentUvIndex.innerHTML = currentUvIndexVal;
    currentLightIntensity.innerHTML = ccurrentLightIntensityVal.toFixed(3);

    // Remove the blur effect etc.
    currentUsageSpinner.style.display = 'none';
    currentUsageOverlay.style.display = 'none';
    currentUsageBlur.forEach((BlurredItem) =>{
        BlurredItem.classList.remove('blur');
    });

    dailyPowerSpinner.style.display = 'none';
    dailyPowerOverlay.style.display = 'none';
    dailyPowerBlur.forEach((BlurredItem) =>{
        BlurredItem.classList.remove('blur');
    });

    lightSpinner.style.display = 'none';
    lightOverlay.style.display = 'none';
    lightBlur.forEach((BlurredItem) =>{
        BlurredItem.classList.remove('blur');
    });
};

/**
 * Get raw dashboard data.
 *
 * @method getData
 */
const getData = () => {
    fetch('/dataajax/?dashboard=solar')
        .then((response) => response.json())
        .then((data) => updateDashboard(data));
};

/**
 * Script entry point.
 *
 * @method init
 *
 */
export const init = () => {
    // Setup auto retrieving of data.
    setup(getData);

    // Get initial data to kick things off.
    getData();
};

