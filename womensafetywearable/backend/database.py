import sqlite3
from datetime import datetime

DATABASE = "safety.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():

    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS device_status (
            id INTEGER PRIMARY KEY,
            device_id TEXT NOT NULL,
            battery INTEGER DEFAULT 0,
            latitude REAL,
            longitude REAL,
            status TEXT DEFAULT 'OFFLINE',
            last_seen TEXT
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            battery INTEGER,
            message TEXT,
            timestamp TEXT NOT NULL
        )
    """)

    # Create initial device
    existing_device = connection.execute("""
        SELECT id FROM device_status WHERE id = 1
    """).fetchone()

    if existing_device is None:

        connection.execute("""
            INSERT INTO device_status
            (
                id,
                device_id,
                battery,
                latitude,
                longitude,
                status,
                last_seen
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            1,
            "WSW-001",
            0,
            None,
            None,
            "OFFLINE",
            None
        ))

    connection.commit()
    connection.close()


def update_device(
    device_id,
    battery,
    latitude,
    longitude,
    status
):

    connection = get_connection()

    timestamp = datetime.utcnow().isoformat()

    connection.execute("""
        UPDATE device_status
        SET
            device_id = ?,
            battery = ?,
            latitude = ?,
            longitude = ?,
            status = ?,
            last_seen = ?
        WHERE id = 1
    """, (
        device_id,
        battery,
        latitude,
        longitude,
        status,
        timestamp
    ))

    connection.commit()
    connection.close()

    return timestamp


def add_alert(
    device_id,
    alert_type,
    latitude,
    longitude,
    battery,
    message
):

    connection = get_connection()

    timestamp = datetime.utcnow().isoformat()

    connection.execute("""
        INSERT INTO alerts
        (
            device_id,
            alert_type,
            latitude,
            longitude,
            battery,
            message,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        device_id,
        alert_type,
        latitude,
        longitude,
        battery,
        message,
        timestamp
    ))

    connection.commit()
    connection.close()

    return timestamp


def get_device():

    connection = get_connection()

    device = connection.execute("""
        SELECT *
        FROM device_status
        WHERE id = 1
    """).fetchone()

    connection.close()

    if device is None:
        return None

    return dict(device)


def get_alerts():

    connection = get_connection()

    alerts = connection.execute("""
        SELECT *
        FROM alerts
        ORDER BY id DESC
        LIMIT 20
    """).fetchall()

    connection.close()

    return [
        dict(alert)
        for alert in alerts
    ]


def clear_active_sos():

    connection = get_connection()

    timestamp = datetime.utcnow().isoformat()

    connection.execute("""
        UPDATE device_status
        SET
            status = 'SAFE',
            last_seen = ?
        WHERE id = 1
    """, (timestamp,))

    connection.commit()
    connection.close()