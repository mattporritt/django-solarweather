// @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
"use strict";import{setup}from"./controls.js";class WeatherChartConfig{constructor(){this.config={type:"line",data:{labels:[],datasets:[{backgroundColor:"#c68200",borderColor:"#FF8C00",data:[]}]},options:{responsive:!0,maintainAspectRatio:!1,plugins:{legend:{display:!1}},scales:{x:{grid:{color:"rgb(255, 255, 255, 0.5)"},ticks:{color:"rgb(255, 255, 255)"}},y:{grid:{color:"rgb(255, 255, 255, 0.5)"},ticks:{color:"rgb(255, 255, 255)"}}}}}}}let Chart;const weatherCharts={indoorTemp:{id:"indoor-temp-chart",chartObj:null,dataLabel:"indoor_temp"},outdoorTemp:{id:"outdoor-temp-chart",chartObj:null,dataLabel:"outdoor_temp"}},updateGraphs=(e,t)=>{weatherCharts[e].chartObj.data.labels=t.labels,weatherCharts[e].chartObj.data.datasets[0].data=t.values,weatherCharts[e].chartObj.update()},formatDate=e=>{const t=[];return new Promise(((o,r)=>{e.labels.forEach((e=>{const o=new Date(1e3*e),r=o.getHours()+":"+("0"+o.getMinutes()).substr(-2);t.push(r)})),o({labels:t,values:e.values})}))},formatTrend=e=>{const t=[],o=[];return new Promise(((r,a)=>{e.forEach((e=>{t.push(e[0]),o.push(e[1])})),r({labels:t,values:o})}))},updateDashboard=e=>{const t=document.getElementById("dashboard-indoor-temp-card"),o=t.querySelector(".loading-spinner"),r=t.querySelector(".overlay"),a=t.querySelectorAll(".blur"),n=document.getElementById("dashboard-outdoor-temp-card"),s=n.querySelector(".loading-spinner"),d=n.querySelector(".overlay"),l=n.querySelectorAll(".blur"),i=document.getElementById("indoor-temp-now"),m=document.getElementById("indoor-temp-now-feels-like"),u=document.getElementById("indoor-temp-day-min"),p=document.getElementById("indoor-temp-day-max"),c=document.getElementById("outdoor-temp-now"),h=document.getElementById("outdoor-temp-now-feels-like"),y=document.getElementById("outdoor-temp-day-min"),b=document.getElementById("outdoor-temp-day-max"),g=e.indoor_temp.latest?e.indoor_temp.latest:0,f=e.indoor_feels_temp.latest?e.indoor_temp.latest:0,w=e.outdoor_temp.latest?e.outdoor_temp.latest:0,_=e.outdoor_feels_temp.latest?e.outdoor_feels_temp.latest:0;i.innerHTML=Number.parseFloat(g).toFixed(1),m.innerHTML=Number.parseFloat(f).toFixed(1),u.innerHTML=Number.parseFloat(e.indoor_temp.daily_min).toFixed(1),p.innerHTML=Number.parseFloat(e.indoor_temp.daily_max).toFixed(1),c.innerHTML=Number.parseFloat(w).toFixed(1),h.innerHTML=Number.parseFloat(_).toFixed(1),y.innerHTML=Number.parseFloat(e.outdoor_temp.daily_min).toFixed(1),b.innerHTML=Number.parseFloat(e.outdoor_temp.daily_max).toFixed(1);for(const t in weatherCharts)if({}.hasOwnProperty.call(weatherCharts,t)){const o=weatherCharts[t].dataLabel;formatTrend(e[o].daily_trend).then(formatDate).then((e=>{updateGraphs(t,e)}))}o.style.display="none",r.style.display="none",a.forEach((e=>{e.classList.remove("blur")})),s.style.display="none",d.style.display="none",l.forEach((e=>{e.classList.remove("blur")}))},getData=()=>{fetch("/dataajax/").then((e=>e.json())).then((e=>updateDashboard(e)))};export const init=e=>{Chart=e;const t=new WeatherChartConfig;for(const e in weatherCharts)({}).hasOwnProperty.call(weatherCharts,e)&&(weatherCharts[e].chartObj=new Chart(document.getElementById(weatherCharts[e].id),t.config));setup(getData),getData()};