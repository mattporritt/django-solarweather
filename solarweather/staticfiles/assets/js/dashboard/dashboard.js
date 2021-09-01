// @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
"use strict";import{setup}from"./controls.js";class WeatherChartConfig{constructor(){this.config={type:"line",data:{labels:[],datasets:[{backgroundColor:"#c68200",borderColor:"#FF8C00",data:[]}]},options:{responsive:!0,maintainAspectRatio:!1,plugins:{legend:{display:!1}},scales:{x:{grid:{color:"rgb(255, 255, 255, 0.5)"},ticks:{color:"rgb(255, 255, 255)"}},y:{grid:{color:"rgb(255, 255, 255, 0.5)"},ticks:{color:"rgb(255, 255, 255)"}}}}}}}let Chart;const weatherCharts={indoorTemp:{id:"indoor-temp-chart",chartObj:null,dataLabel:"indoor_temp"},outdoorTemp:{id:"outdoor-temp-chart",chartObj:null,dataLabel:"outdoor_temp"}},windDegrees=["N","NE","E","SE","S","SW","W","NW"],updateGraphs=(e,t)=>{weatherCharts[e].chartObj.data.labels=t.labels,weatherCharts[e].chartObj.data.datasets[0].data=t.values,weatherCharts[e].chartObj.update()},formatDate=e=>{const t=[];return new Promise(((r,o)=>{e.labels.forEach((e=>{const r=new Date(1e3*e),o=r.getHours()+":"+("0"+r.getMinutes()).substr(-2);t.push(o)})),r({labels:t,values:e.values})}))},formatTrend=e=>{const t=[],r=[];return new Promise(((o,n)=>{e.forEach((e=>{t.push(e[0]),r.push(e[1])})),o({labels:t,values:r})}))},updateDashboard=e=>{const t=document.getElementById("dashboard-indoor-temp-card"),r=t.querySelector(".loading-spinner"),o=t.querySelector(".overlay"),n=t.querySelectorAll(".blur"),a=document.getElementById("dashboard-outdoor-temp-card"),d=a.querySelector(".loading-spinner"),l=a.querySelector(".overlay"),i=a.querySelectorAll(".blur"),s=document.getElementById("dashboard-humidity-card"),m=s.querySelector(".loading-spinner"),u=s.querySelector(".overlay"),y=s.querySelectorAll(".blur"),c=document.getElementById("dashboard-rain-card"),p=c.querySelector(".loading-spinner"),h=c.querySelector(".overlay"),b=c.querySelectorAll(".blur"),g=document.getElementById("dashboard-pressure-card"),_=g.querySelector(".loading-spinner"),E=g.querySelector(".overlay"),w=g.querySelectorAll(".blur"),F=document.getElementById("dashboard-wind-card"),I=F.querySelector(".loading-spinner"),L=F.querySelector(".overlay"),x=F.querySelectorAll(".blur"),B=document.getElementById("indoor-temp-now"),N=document.getElementById("indoor-temp-now-feels-like"),T=document.getElementById("indoor-temp-day-min"),H=document.getElementById("indoor-temp-day-max"),f=document.getElementById("outdoor-temp-now"),M=document.getElementById("outdoor-temp-now-feels-like"),C=document.getElementById("outdoor-temp-day-min"),S=document.getElementById("outdoor-temp-day-max"),q=document.getElementById("indoor-humidity-now"),v=document.getElementById("indoor-humidity-day-min"),D=document.getElementById("indoor-humidity-day-max"),j=document.getElementById("outdoor-humidity-now"),O=document.getElementById("outdoor-humidity-day-min"),k=document.getElementById("outdoor-humidity-day-max"),A=document.getElementById("rain-day"),W=document.getElementById("rain-rate"),P=document.getElementById("rain-week"),G=document.getElementById("rain-month"),R=document.getElementById("pressure-now"),z=document.getElementById("pressure-day-min"),J=document.getElementById("pressure-day-max"),K=document.getElementById("wind-now"),Q=document.getElementById("wind-dir"),U=document.getElementById("wind-day-min"),V=document.getElementById("wind-day-max"),X=document.getElementById("wind-gust"),Y=e.indoor_temp.latest?e.indoor_temp.latest:0,Z=e.indoor_feels_temp.latest?e.indoor_feels_temp.latest:0,$=e.outdoor_temp.latest?e.outdoor_temp.latest:0,ee=e.outdoor_feels_temp.latest?e.outdoor_feels_temp.latest:0,te=e.indoor_humidity.latest?e.indoor_humidity.latest:0,re=e.outdoor_humidity.latest?e.outdoor_humidity.latest:0,oe=(new Date).getHours()+1,ne=e.daily_rain.latest/oe,ae=Number.parseInt(e.wind_direction.latest/45+.5),de=windDegrees[ae]?windDegrees[ae]:"N";B.innerHTML=Number.parseFloat(Y).toFixed(1),N.innerHTML=Number.parseFloat(Z).toFixed(1),T.innerHTML=Number.parseFloat(e.indoor_temp.daily_min).toFixed(1),H.innerHTML=Number.parseFloat(e.indoor_temp.daily_max).toFixed(1),f.innerHTML=Number.parseFloat($).toFixed(1),M.innerHTML=Number.parseFloat(ee).toFixed(1),C.innerHTML=Number.parseFloat(e.outdoor_temp.daily_min).toFixed(1),S.innerHTML=Number.parseFloat(e.outdoor_temp.daily_max).toFixed(1),q.innerHTML=Number.parseInt(te),v.innerHTML=Number.parseInt(e.indoor_humidity.daily_min),D.innerHTML=Number.parseInt(e.indoor_humidity.daily_max),j.innerHTML=Number.parseInt(re),O.innerHTML=Number.parseInt(e.outdoor_humidity.daily_min),k.innerHTML=Number.parseInt(e.outdoor_humidity.daily_max),A.innerHTML=Number.parseFloat(e.daily_rain.latest).toFixed(1),W.innerHTML=Number.parseFloat(ne).toFixed(1),P.innerHTML=Number.parseFloat(e.weekly_rain.latest).toFixed(1),G.innerHTML=Number.parseFloat(e.monthly_rain.latest).toFixed(1),R.innerHTML=Number.parseFloat(e.pressure.latest).toFixed(2),z.innerHTML=Number.parseFloat(e.pressure.daily_min).toFixed(2),J.innerHTML=Number.parseFloat(e.pressure.daily_max).toFixed(2),K.innerHTML=Number.parseFloat(e.wind_speed.latest).toFixed(1),Q.innerHTML=de,U.innerHTML=Number.parseFloat(e.wind_speed.daily_min).toFixed(1),V.innerHTML=Number.parseFloat(e.wind_speed.daily_max).toFixed(1),X.innerHTML=Number.parseFloat(e.wind_gust.latest).toFixed(1);for(const t in weatherCharts)if({}.hasOwnProperty.call(weatherCharts,t)){const r=weatherCharts[t].dataLabel;formatTrend(e[r].daily_trend).then(formatDate).then((e=>{updateGraphs(t,e)}))}r.style.display="none",o.style.display="none",n.forEach((e=>{e.classList.remove("blur")})),d.style.display="none",l.style.display="none",i.forEach((e=>{e.classList.remove("blur")})),m.style.display="none",u.style.display="none",y.forEach((e=>{e.classList.remove("blur")})),p.style.display="none",h.style.display="none",b.forEach((e=>{e.classList.remove("blur")})),_.style.display="none",E.style.display="none",w.forEach((e=>{e.classList.remove("blur")})),I.style.display="none",L.style.display="none",x.forEach((e=>{e.classList.remove("blur")}))},getData=()=>{fetch("/dataajax/").then((e=>e.json())).then((e=>updateDashboard(e)))};export const init=e=>{Chart=e;const t=new WeatherChartConfig;for(const e in weatherCharts)({}).hasOwnProperty.call(weatherCharts,e)&&(weatherCharts[e].chartObj=new Chart(document.getElementById(weatherCharts[e].id),t.config));setup(getData),getData()};