import os
import json
import time
import random
from datetime import datetime
from google.cloud import pubsub_v1

project_id = os.getenv("GCP_PROJECT_ID", "test-project")
topic_id = os.getenv("PUBSUB_TOPIC_RAW", "iot-sensor-data-raw")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def generate_sensor_data():
    return {
        "device_id": "device_1",
        "timestamp_utc": datetime.utcnow().isoformat(),
        "temperature_celsius": round(random.uniform(-10, 50), 2),
        "humidity_percent": round(random.uniform(20, 90), 2)
    }

while True:
    data = generate_sensor_data()
    message = json.dumps(data).encode("utf-8")
    publisher.publish(topic_path, message)
    print("Published:", data)
    time.sleep(2)
