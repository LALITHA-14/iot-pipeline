import os
from google.cloud import pubsub_v1

# IMPORTANT: emulator connection
os.environ["PUBSUB_EMULATOR_HOST"] = "pubsub-emulator:8085"

project_id = "test-project"
topic_id = "iot-sensor-data-raw"
subscription_id = "iot-sub"

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

topic_path = publisher.topic_path(project_id, topic_id)
subscription_path = subscriber.subscription_path(project_id, subscription_id)

# Create topic
try:
    publisher.create_topic(name=topic_path)
    print("✅ Topic created")
except Exception as e:
    print("Topic exists:", e)

# Create subscription
try:
    subscriber.create_subscription(
        name=subscription_path,
        topic=topic_path
    )
    print("✅ Subscription created")
except Exception as e:
    print("Subscription exists:", e)

print("🚀 Pub/Sub emulator initialized!")
