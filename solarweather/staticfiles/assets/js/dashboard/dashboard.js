// @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
"use strict";import{setup}from"./controls.js";const printOut=()=>{window.console.log("Timer expired.")};export const init=()=>{window.console.log("Dashboard JS loaded."),setup(printOut),fetch("/dataajax/").then((o=>o.json())).then((o=>window.console.log(o)))};