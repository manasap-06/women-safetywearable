from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

from database import (
    initialize_database,
    update_device,
    add_alert,
    get_device,
    get_alerts,
    clear_active_sos
)


app = Flask(__name__)

CORS(app)


# ==================================================
# START DATABASE
# ==================================================

initialize_database()


# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():

    return jsonify({
        "system": "Women Safety Wearable",
        "backend": "Flask",
        "status": "online",
        "message": "Women Safety Wearable API is running"
    })


# ==================================================
# HEALTH CHECK
# ==================================================

@app.route("/api/health")
def health():

    return jsonify({
        "status": "online",
        "timestamp": datetime.utcnow().isoformat()
    })


# ==================================================
# RECEIVE DATA FROM ESP32 / WEARABLE
# ==================================================

@app.route("/api/wearable/data", methods=["POST"])
def wearable_data():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message": "No JSON data received"
        }), 400


    device_id = data.get(
        "device_id",
        "WSW-001"
    )

    alert_type = data.get(
        "alert_type",
        "NORMAL"
    )

    latitude = data.get(
        "latitude"
    )

    longitude = data.get(
        "longitude"
    )

    battery = data.get(
        "battery",
        0
    )

    message = data.get(
        "message",
        ""
    )


    # ----------------------------------------------
    # Determine device status
    # ----------------------------------------------

    if alert_type == "SOS":

        status = "SOS"

    elif alert_type == "FALL":

        status = "FALL"

    else:

        status = "SAFE"


    # ----------------------------------------------
    # Update latest device information
    # ----------------------------------------------

    timestamp = update_device(
        device_id,
        battery,
        latitude,
        longitude,
        status
    )


    # ----------------------------------------------
    # Save alert
    # ----------------------------------------------

    if alert_type != "NORMAL":

        add_alert(
            device_id,
            alert_type,
            latitude,
            longitude,
            battery,
            message
        )


    return jsonify({
        "success": True,
        "message": "Wearable data received",
        "device_id": device_id,
        "status": status,
        "timestamp": timestamp
    })


# ==================================================
# GET CURRENT DEVICE STATUS
# ==================================================

@app.route("/api/device")
def device():

    device_data = get_device()

    if device_data is None:

        return jsonify({
            "success": False,
            "message": "Device not found"
        }), 404


    return jsonify(device_data)


# ==================================================
# GET ALERT HISTORY
# ==================================================

@app.route("/api/alerts")
def alerts():

    return jsonify(
        get_alerts()
    )


# ==================================================
# TEST SOS
# ==================================================

@app.route("/api/test/sos", methods=["POST"])
def test_sos():

    device_id = "WSW-001"

    battery = 87

    latitude = 17.6868

    longitude = 83.2185

    message = "Emergency SOS triggered"


    timestamp = update_device(
        device_id,
        battery,
        latitude,
        longitude,
        "SOS"
    )


    add_alert(
        device_id,
        "SOS",
        latitude,
        longitude,
        battery,
        message
    )


    return jsonify({
        "success": True,
        "message": "Test SOS generated",
        "timestamp": timestamp
    })


# ==================================================
# TEST FALL
# ==================================================

@app.route("/api/test/fall", methods=["POST"])
def test_fall():

    device_id = "WSW-001"

    battery = 82

    latitude = 17.6868

    longitude = 83.2185

    message = "Possible fall detected"


    timestamp = update_device(
        device_id,
        battery,
        latitude,
        longitude,
        "FALL"
    )


    add_alert(
        device_id,
        "FALL",
        latitude,
        longitude,
        battery,
        message
    )


    return jsonify({
        "success": True,
        "message": "Test fall alert generated",
        "timestamp": timestamp
    })


# ==================================================
# RESET DEVICE
# ==================================================

@app.route("/api/test/reset", methods=["POST"])
def reset():

    clear_active_sos()

    return jsonify({
        "success": True,
        "message": "Device returned to SAFE status"
    })


# ==================================================
# RUN SERVER
# ==================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )