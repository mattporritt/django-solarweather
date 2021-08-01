
// ==============================================================================
//
// This file is part of ActiveAudit.
//
// ActiveAudit is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// ActiveAudit is distributed  WITHOUT ANY WARRANTY:
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

let refreshPeriod = 60;
let counterid;
let callback;

/**
 * Handle processing of refresh and period button actions.
 *
 * @param {Event} event The triggered event for the element.
 */
const refreshAction = (event) => {
    event.preventDefault();
    const element = event.target;

    if (element.closest('button') !== null && element.closest('button').id === 'refresh-dashboard') {
        callback();
    } else if (element.tagName.toLowerCase() === 'a') {
        refreshPeriod = element.dataset.period;

        const refreshElement = document.getElementById('period-container');
        const actionButton = refreshElement.getElementsByClassName('dropdown-toggle')[0];
        actionButton.textContent = element.innerHTML;

        const activeoptions = refreshElement.getElementsByClassName('active');

        // Fix active classes.
        for (let i = 0; i < activeoptions.length; i++) {
            activeoptions[i].classList.remove('active');
        }
        element.classList.add('active');
    }

    refreshCounter(true);
};

/**
 * Function for refreshing the counter.
 *
 * @param {boolean} reset Reset the current count process.
 */
const refreshCounter = (reset = true) => {
    const progressElement = document.getElementById('refresh-progress');

    // Reset the current count process.
    if (reset === true) {
        clearInterval(counterid);
        counterid = null;
        progressElement.setAttribute('style', 'width: 100%');
        progressElement.setAttribute('aria-valuenow', '100');
    }

    // Exit early if there is already a counter running.
    if (counterid) {
        return;
    }

    counterid = setInterval(() => {
        const progressWidthAria = progressElement.getAttribute('aria-valuenow');
        const progressStep = 100 / refreshPeriod;

        if ((progressWidthAria - progressStep) > 0) {
            progressElement.setAttribute('style', 'width: ' + (progressWidthAria - progressStep) + '%');
            progressElement.setAttribute('aria-valuenow', String(progressWidthAria - progressStep));
        } else {
            clearInterval(counterid);
            counterid = null;
            progressElement.setAttribute('style', 'width: 100%');
            progressElement.setAttribute('aria-valuenow', '100');
            callback();
            refreshCounter();
        }
    }, (1000));
};

/**
 * External entry point to set up the refresh counter.
 *
 * @param {function} callbackfunc The function to call when the counter reaches zero..
 */
export const setup = (callbackfunc) => {
    callback = callbackfunc;

    // Event handling for refresh and period buttons.
    const refreshElement = document.getElementById('period-container');
    refreshElement.addEventListener('click', refreshAction);

    // Start the refresh counter.
    refreshCounter();
};
