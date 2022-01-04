const STATS_ENDPOINT = "http://127.0.0.1:5000/api/v1/users/new";
const STORAGE_KEY = "__user_stats"

function sendData(method, url, data, callback) {
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = callback;
    xmlhttp.open(method, url, true);
    if (data) {
        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xmlhttp.send(JSON.stringify(data));
    } else {
        xmlhttp.send();
    }
}

function initUserSessionData() {
    let data = JSON.parse(localStorage.getItem(STORAGE_KEY))
    if (!data) {
        data = {
            in_count: 1,
            in_ts: Date.now()
        };
    } else {
        data.in_count += 1; 
    }
    // Race condition risk
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    return data;
}

initUserSessionData();

let userData = {};
userData.ip = '';
userData.url = window.location.hostname || window.location.host;
userData.lang = navigator.language || navigator.userLanguage;
userData.timezone = '' + (new Date().getTimezoneOffset());
userData.os = window.navigator.oscpu;
userData.agent = navigator.userAgent;
userData.resolution = '' + window.screen.availWidth + 'x' + window.screen.availHeight;

window.addEventListener("beforeunload", function(e){
    let userSessionData = JSON.parse(localStorage.getItem(STORAGE_KEY));
    userSessionData.in_count -= 1;
    if (userSessionData.in_count > 0) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(userSessionData));
    } else {
        userData.duration = Date.now() - userSessionData.in_ts;
        localStorage.removeItem(STORAGE_KEY);
        // let callback = function() {
            // if (stats.readyState == XMLHttpRequest.DONE) {
               // if (stats.status == 200) {
                   // localStorage.removeItem(STORAGE_KEY);
                   // return;
               // }
            // }
        // };
        sendData("POST", STATS_ENDPOINT, userData, null);
    }
    return null;
}, false);
