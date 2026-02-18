from google.cloud import pubsub_v1
import os
import json

project_id = "test-project"
topic_id = "iot-sensor-data-raw"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

data = {
    "device_id": "sensor_1",
    "timestamp_utc": "2026-02-18T10:00:00Z",
    "temperature_celsius": 26.5,
    "humidity_percent": 55
}

publisher.publish(topic_path, json.dumps(data).encode())

print("✅ Message published")
