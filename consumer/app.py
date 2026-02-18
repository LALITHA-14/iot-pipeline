import os
import json
import time
from datetime import datetime

from google.cloud import pubsub_v1
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel, ValidationError


# =====================================
# Environment Configuration
# =====================================

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "test-project")

MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "iot_data")

SUBSCRIPTION_ID = "iot-sub"


# =====================================
# Data Validation Model
# =====================================

class SensorData(BaseModel):
    device_id: str
    timestamp_utc: datetime
    temperature_celsius: float
    humidity_percent: float


# =====================================
# MySQL Connection (Retry Until Ready)
# =====================================

def connect_mysql():
    while True:
        try:
            print("🔄 Connecting to MySQL...")

            conn = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE,
            )

            if conn.is_connected():
                print("✅ Connected to MySQL")
                return conn

        except Error as e:
            print(f"⏳ MySQL not ready yet: {e}")
            time.sleep(5)


conn = connect_mysql()
cursor = conn.cursor()


# =====================================
# Message Processing
# =====================================

def process_message(data: bytes) -> bool:
    global conn, cursor

    try:
        payload = json.loads(data.decode("utf-8"))
        validated = SensorData(**payload)

        query = """
        INSERT INTO sensor_readings (
            device_id,
            timestamp_utc,
            temperature_celsius,
            humidity_percent,
            processing_timestamp_utc
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                validated.device_id,
                validated.timestamp_utc,
                validated.temperature_celsius,
                validated.humidity_percent,
                datetime.utcnow(),
            ),
        )

        conn.commit()

        print(f"✅ Inserted data from device: {validated.device_id}")
        return True

    except ValidationError as e:
        print("❌ Validation failed:", e)
        return False

    except mysql.connector.Error as db_error:
        print("⚠️ DB error — reconnecting:", db_error)

        try:
            conn.close()
        except:
            pass

        conn = connect_mysql()
        cursor = conn.cursor()
        return False

    except Exception as e:
        print("❌ Processing error:", e)
        conn.rollback()
        return False


# =====================================
# Pub/Sub Subscriber Setup
# =====================================

# Emulator support (IMPORTANT)
if os.getenv("PUBSUB_EMULATOR_HOST"):
    print("🧪 Using Pub/Sub Emulator:", os.getenv("PUBSUB_EMULATOR_HOST"))

subscriber = pubsub_v1.SubscriberClient()

subscription_path = subscriber.subscription_path(
    PROJECT_ID,
    SUBSCRIPTION_ID,
)


# =====================================
# Callback Function
# =====================================

def callback(message):
    print("📩 Message received")

    success = process_message(message.data)

    if success:
        message.ack()
        print("✅ Message acknowledged")
    else:
        message.nack()
        print("⚠️ Message requeued")


# =====================================
# Start Subscriber
# =====================================

print("🚀 Starting subscriber...")
future = subscriber.subscribe(subscription_path, callback=callback)

print("👂 Listening for messages...")

try:
    future.result()

except KeyboardInterrupt:
    print("🛑 Shutting down subscriber...")
    future.cancel()

finally:
    try:
        conn.close()
        print("🔌 MySQL connection closed")
    except:
        pass
