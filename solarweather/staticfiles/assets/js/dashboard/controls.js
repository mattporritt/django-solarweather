// @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
"use strict";let counterid,callback,refreshPeriod=60;const refreshAction=e=>{e.preventDefault();const t=e.target;if(null!==t.closest("button")&&"refresh-dashboard"===t.closest("button").id)callback();else if("a"===t.tagName.toLowerCase()){refreshPeriod=t.dataset.period;const e=document.getElementById("period-container");e.getElementsByClassName("dropdown-toggle")[0].textContent=t.innerHTML;const r=e.getElementsByClassName("active");for(let e=0;e<r.length;e++)r[e].classList.remove("active");t.classList.add("active")}refreshCounter(!0)},refreshCounter=(e=!0)=>{const t=document.getElementById("refresh-progress");!0===e&&(clearInterval(counterid),counterid=null,t.setAttribute("style","width: 100%"),t.setAttribute("aria-valuenow","100")),counterid||(counterid=setInterval((()=>{const e=t.getAttribute("aria-valuenow"),r=100/refreshPeriod;e-r>0?(t.setAttribute("style","width: "+(e-r)+"%"),t.setAttribute("aria-valuenow",String(e-r))):(clearInterval(counterid),counterid=null,t.setAttribute("style","width: 100%"),t.setAttribute("aria-valuenow","100"),callback(),refreshCounter())}),1e3))};export const setup=e=>{callback=e;document.getElementById("period-container").addEventListener("click",refreshAction),refreshCounter()};