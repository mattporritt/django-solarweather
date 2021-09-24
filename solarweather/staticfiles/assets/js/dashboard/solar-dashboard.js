// @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
"use strict";import{setup}from"./controls.js";const updateDashboard=e=>{const t=document.getElementById("dashboard-current-usage-card"),r=t.querySelector(".loading-spinner"),a=t.querySelector(".overlay"),o=t.querySelectorAll(".blur"),s=document.getElementById("current-usage-now"),n=document.getElementById("current-usage-from-solar"),l=document.getElementById("current-usage-from-grid"),u=e.power_consumption.latest?e.power_consumption.latest:0,d=e.inverter_ac_power.latest?e.inverter_ac_power.latest:0,c=e.grid_power_usage_real.latest?e.grid_power_usage_real.latest:0,i=Number.parseFloat(u)/1e3,p=Number.parseFloat(d)/1e3,m=Number.parseFloat(c)/1e3;s.innerHTML=i.toFixed(3),n.innerHTML=p.toFixed(3),l.innerHTML=m.toFixed(3),r.style.display="none",a.style.display="none",o.forEach((e=>{e.classList.remove("blur")}))},getData=()=>{fetch("/dataajax/?dashboard=solar").then((e=>e.json())).then((e=>updateDashboard(e)))};export const init=()=>{setup(getData),getData()};