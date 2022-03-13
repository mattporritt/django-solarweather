// @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
"use strict";const solarCharts={energyBalance:{id:"energy-balance-chart",chartObj:null,dataLabel:"grid_power_usage_real",type:"bar",invert:!0,suggestedMinVal:-5e3,suggestedMaxVal:5e3},generation:{id:"solar-generation-chart",chartObj:null,dataLabel:"inverter_ac_power",type:"line",invert:!1,suggestedMinVal:0,suggestedMaxVal:5e3}};class SolarChartConfig{constructor(e,t,r){this.config={type:e,data:{labels:[],datasets:[{backgroundColor:"#c68200",borderColor:"#FF8C00",data:[]}]},options:{responsive:!0,maintainAspectRatio:!1,plugins:{legend:{display:!1}},scales:{x:{grid:{color:"rgb(255, 255, 255, 0.5)"},ticks:{color:"rgb(255, 255, 255)"}},y:{grid:{color:"rgb(255, 255, 255, 0.5)"},ticks:{color:"rgb(255, 255, 255)"},suggestedMin:-5e3,suggestedMax:5e3}}}},void 0!==t&&(this.config.options.scales.y.suggestedMin=t),void 0!==r&&(this.config.options.scales.y.suggestedMax=r)}}let Chart;const updateGraphs=(e,t)=>{solarCharts[e].chartObj.data.labels=t.labels,solarCharts[e].chartObj.data.datasets[0].data=t.values,solarCharts[e].chartObj.update()},formatDate=e=>{const t=[];return new Promise(((r,a)=>{e.labels.forEach((e=>{const r=new Date(1e3*e),a=r.getHours()+":"+("0"+r.getMinutes()).substr(-2);t.push(a)})),r({labels:t,values:e.values})}))},formatTrend=(e,t)=>{const r=[],a=[];return new Promise(((o,n)=>{e.forEach((e=>{r.push(e[0]),!0===t?a.push(-1*e[1]):a.push(e[1])})),o({labels:r,values:a})}))},updateDashboard=e=>{const t=document.getElementById("dashboard-current-usage-card"),r=t.querySelector(".loading-spinner"),a=t.querySelector(".overlay"),o=t.querySelectorAll(".blur"),n=document.getElementById("dashboard-daily-power-card"),s=n.querySelector(".loading-spinner"),l=n.querySelector(".overlay"),d=n.querySelectorAll(".blur"),i=document.getElementById("dashboard-light-card"),c=i.querySelector(".loading-spinner"),u=i.querySelector(".overlay"),g=i.querySelectorAll(".blur"),y=document.getElementById("dashboard-energy-balance-card"),m=y.querySelector(".loading-spinner"),p=y.querySelector(".overlay"),h=y.querySelectorAll(".blur"),b=document.getElementById("dashboard-solar-generation-card"),_=b.querySelector(".loading-spinner"),v=b.querySelector(".overlay"),w=b.querySelectorAll(".blur"),E=document.getElementById("current-usage-now"),C=document.getElementById("current-usage-from-solar"),f=document.getElementById("current-usage-from-grid"),M=document.getElementById("generated-day"),x=document.getElementById("generated-week"),F=document.getElementById("generated-month"),L=document.getElementById("used-day"),B=document.getElementById("used-week"),I=document.getElementById("used-month"),S=document.getElementById("uv-index"),q=document.getElementById("light-intensity"),T=document.getElementById("energy-balance-surplus"),H=document.getElementById("solar-generation-total"),N=e.power_consumption.latest?e.power_consumption.latest:0,k=e.inverter_ac_power.latest?e.inverter_ac_power.latest:0,j=e.grid_power_usage_real.latest?e.grid_power_usage_real.latest:0,A=e.inverter_ac_power.day?e.inverter_ac_power.day:0,D=e.inverter_ac_power.week?e.inverter_ac_power.week:0,O=e.inverter_ac_power.month?e.inverter_ac_power.month:0,V=e.power_consumption.day?e.power_consumption.day:0,P=e.power_consumption.week?e.power_consumption.week:0,G=e.power_consumption.month?e.power_consumption.month:0,R=e.uv_index.latest?e.uv_index.latest:0,z=e.solar_radiation.latest?e.solar_radiation.latest:0,J=Number.parseFloat(N)/1e3,K=Number.parseFloat(k)/1e3,Q=Number.parseFloat(j)/1e3,U=Number.parseFloat(A)/1e3,W=Number.parseFloat(D)/1e3,X=Number.parseFloat(O)/1e3,Y=Number.parseFloat(V)/1e3,Z=Number.parseFloat(P)/1e3,$=Number.parseFloat(G)/1e3,ee=U-Y;E.innerHTML=J.toFixed(3),C.innerHTML=K.toFixed(3),f.innerHTML=Q.toFixed(3),M.innerHTML=U.toFixed(3),x.innerHTML=W.toFixed(1),F.innerHTML=X.toFixed(1),L.innerHTML=Y.toFixed(3),B.innerHTML=Z.toFixed(1),I.innerHTML=$.toFixed(1),S.innerHTML=R,q.innerHTML=z.toFixed(2),T.innerHTML=ee.toFixed(3),H.innerHTML=U.toFixed(3);for(const t in solarCharts)if({}.hasOwnProperty.call(solarCharts,t)){const r=solarCharts[t].dataLabel;formatTrend(e[r].daily_trend,solarCharts[t].invert).then(formatDate).then((e=>{updateGraphs(t,e)}))}r.style.display="none",a.style.display="none",o.forEach((e=>{e.classList.remove("blur")})),s.style.display="none",l.style.display="none",d.forEach((e=>{e.classList.remove("blur")})),c.style.display="none",u.style.display="none",g.forEach((e=>{e.classList.remove("blur")})),m.style.display="none",p.style.display="none",h.forEach((e=>{e.classList.remove("blur")})),_.style.display="none",v.style.display="none",w.forEach((e=>{e.classList.remove("blur")}))},getData=e=>{fetch("/dataajax/?dashboard=solar&timestamp="+e).then((e=>e.json())).then((e=>updateDashboard(e)))},dateChange=e=>{const t=e.target.valueAsNumber/1e3;getData(t)};export const init=e=>{Chart=e;for(const e in solarCharts)if({}.hasOwnProperty.call(solarCharts,e)){const t=new SolarChartConfig(solarCharts[e].type,solarCharts[e].suggestedMinVal,solarCharts[e].suggestedMaxVal);solarCharts[e].chartObj=new Chart(document.getElementById(solarCharts[e].id),t.config)}const t=document.getElementById("history-date");t.addEventListener("change",dateChange);const r=t.valueAsNumber/1e3;getData(r)};