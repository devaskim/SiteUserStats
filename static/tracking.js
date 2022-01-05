const STATS_ENDPOINT = "http://127.0.0.1:5000/api/v1/users/new";
const IP_ENDPOINT = "http://127.0.0.1:5000/api/v1/ip";
const STORAGE_KEY = "__user_stats"

function sendData(method, url, data, callback) {
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(callback) {
        if (callback == null) {
            return;
        }
        if (this.readyState === XMLHttpRequest.DONE) {
            if (this.status === 200) {
                callback(JSON.parse(this.responseText));
            }
        }
    }.bind(xhr, callback);
    xhr.open(method, url, true);

    if (data) {
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify(data));
    } else {
        xhr.send();
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

let userData = {
    ip: "",
    url: window.location.hostname || window.location.host,
    lang: navigator.language || navigator.userLanguage,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    os: window.navigator.oscpu,
    agent: navigator.userAgent,
    resolution: '' + window.screen.availWidth + 'x' + window.screen.availHeight
};

sendData("GET", IP_ENDPOINT, null, function(data) {
    userData.ip = data.ip;
});

window.addEventListener("beforeunload", function(e){
    let userSessionData = JSON.parse(localStorage.getItem(STORAGE_KEY));
    userSessionData.in_count -= 1;
    if (userSessionData.in_count > 0) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(userSessionData));
    } else {
        userData.duration = Date.now() - userSessionData.in_ts;
        localStorage.removeItem(STORAGE_KEY);
        sendData("POST", STATS_ENDPOINT, userData);
    }
    return null;
}, false);
