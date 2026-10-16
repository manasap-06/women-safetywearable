// ==================================================
// BACKEND URL
// ==================================================

const API_URL = "https://women-safetywearable-ba54.onrender.com";


// ==================================================
// CHECK BACKEND
// ==================================================

async function checkBackend() {

    try {

        const response =
            await fetch(
                `${API_URL}/api/health`
            );


        if (!response.ok) {

            throw new Error(
                "Backend unavailable"
            );

        }


        const data =
            await response.json();


        const status =
            document.getElementById(
                "connectionStatus"
            );


        status.textContent =
            "● BACKEND ONLINE";


        status.className =
            "connection online";

    }

    catch (error) {

        const status =
            document.getElementById(
                "connectionStatus"
            );


        status.textContent =
            "● BACKEND OFFLINE";


        status.className =
            "connection offline";

    }

}



// ==================================================
// LOAD DEVICE
// ==================================================

async function loadDevice() {

    try {

        const response =
            await fetch(
                `${API_URL}/api/device`
            );


        const device =
            await response.json();


        document.getElementById(
            "deviceId"
        ).textContent =
            device.device_id;


        document.getElementById(
            "deviceStatus"
        ).textContent =
            device.status;


        document.getElementById(
            "battery"
        ).textContent =
            `${device.battery}%`;


        document.getElementById(
            "batteryBar"
        ).style.width =
            `${device.battery}%`;


        document.getElementById(
            "latitude"
        ).textContent =
            device.latitude !== null
                ? device.latitude
                : "--";


        document.getElementById(
            "longitude"
        ).textContent =
            device.longitude !== null
                ? device.longitude
                : "--";


        document.getElementById(
            "lastSeen"
        ).textContent =
            formatTime(device.last_seen);


        updateEmergency(
            device.status
        );

    }

    catch (error) {

        console.log(
            "Device error:",
            error
        );

    }

}



// ==================================================
// EMERGENCY DISPLAY
// ==================================================

function updateEmergency(status) {

    const card =
        document.getElementById(
            "emergencyCard"
        );


    const title =
        document.getElementById(
            "emergencyTitle"
        );


    const message =
        document.getElementById(
            "emergencyMessage"
        );


    const icon =
        document.querySelector(
            ".emergency-icon"
        );


    // -----------------------------
    // SOS
    // -----------------------------

    if (status === "SOS") {

        card.className =
            "emergency danger";


        icon.textContent =
            "🚨";


        title.textContent =
            "SOS ALERT";


        message.textContent =
            "Emergency signal received from wearable.";

    }


    // -----------------------------
    // FALL
    // -----------------------------

    else if (status === "FALL") {

        card.className =
            "emergency fall";


        icon.textContent =
            "⚠️";


        title.textContent =
            "FALL DETECTED";


        message.textContent =
            "Possible fall detected by wearable.";

    }


    // -----------------------------
    // SAFE
    // -----------------------------

    else {

        card.className =
            "emergency safe";


        icon.textContent =
            "🛡️";


        title.textContent =
            "SYSTEM SAFE";


        message.textContent =
            "No active emergency detected.";

    }

}



// ==================================================
// LOAD ALERTS
// ==================================================

async function loadAlerts() {

    try {

        const response =
            await fetch(
                `${API_URL}/api/alerts`
            );


        const alerts =
            await response.json();


        const container =
            document.getElementById(
                "alerts"
            );


        const count =
            document.getElementById(
                "alertCount"
            );


        count.textContent =
            `${alerts.length} alerts`;


        if (alerts.length === 0) {

            container.innerHTML = `

                <div class="empty">

                    No alerts recorded.

                </div>

            `;

            return;

        }


        container.innerHTML = "";


        alerts.forEach(
            function(alert) {


                const item =
                    document.createElement(
                        "div"
                    );


                item.className =
                    "alert-item";


                if (
                    alert.alert_type ===
                    "FALL"
                ) {

                    item.classList.add(
                        "fall-alert"
                    );

                }


                item.innerHTML = `

                    <div class="alert-header">

                        <span class="alert-type">

                            ${
                                alert.alert_type
                            }

                        </span>

                        <span class="alert-time">

                            ${
                                formatTime(
                                    alert.timestamp
                                )
                            }

                        </span>

                    </div>


                    <div class="alert-details">

                        <strong>
                            Device:
                        </strong>

                        ${
                            alert.device_id
                        }

                        <br>


                        <strong>
                            Battery:
                        </strong>

                        ${
                            alert.battery
                        }%


                        <br>


                        <strong>
                            Location:
                        </strong>

                        ${
                            alert.latitude
                        },
                        ${
                            alert.longitude
                        }


                        <br>


                        <strong>
                            Message:
                        </strong>

                        ${
                            alert.message
                        }

                    </div>

                `;


                container.appendChild(
                    item
                );

            }
        );

    }

    catch (error) {

        console.log(
            "Alert error:",
            error
        );

    }

}



// ==================================================
// TEST SOS
// ==================================================

async function triggerSOS() {

    try {

        const response =
            await fetch(
                `${API_URL}/api/test/sos`,
                {
                    method: "POST"
                }
            );


        if (!response.ok) {

            throw new Error(
                "SOS request failed"
            );

        }


        await refreshDashboard();

    }

    catch (error) {

        alert(
            "Backend is not running."
        );

    }

}



// ==================================================
// TEST FALL
// ==================================================

async function triggerFall() {

    try {

        const response =
            await fetch(
                `${API_URL}/api/test/fall`,
                {
                    method: "POST"
                }
            );


        if (!response.ok) {

            throw new Error(
                "Fall request failed"
            );

        }


        await refreshDashboard();

    }

    catch (error) {

        alert(
            "Backend is not running."
        );

    }

}



// ==================================================
// RESET
// ==================================================

async function resetDevice() {

    try {

        const response =
            await fetch(
                `${API_URL}/api/test/reset`,
                {
                    method: "POST"
                }
            );


        if (!response.ok) {

            throw new Error(
                "Reset failed"
            );

        }


        await refreshDashboard();

    }

    catch (error) {

        alert(
            "Backend is not running."
        );

    }

}



// ==================================================
// TIME FORMAT
// ==================================================

function formatTime(timestamp) {

    if (!timestamp) {

        return "--";

    }


    const date =
        new Date(timestamp);


    if (isNaN(date.getTime())) {

        return timestamp;

    }


    return date.toLocaleString();

}



// ==================================================
// REFRESH DASHBOARD
// ==================================================

async function refreshDashboard() {

    await checkBackend();

    await loadDevice();

    await loadAlerts();

}



// ==================================================
// INITIAL LOAD
// ==================================================

refreshDashboard();



// ==================================================
// REAL-TIME REFRESH
// ==================================================

// Every 2 seconds the website
// asks Flask for the newest data.

setInterval(
    refreshDashboard,
    2000
);
