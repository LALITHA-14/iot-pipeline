import os
from google.cloud import pubsub_v1

project_id = os.getenv("GCP_PROJECT_ID", "test-project")

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

topic_id = "iot-sensor-data-raw"
subscription_id = "iot-sub"

topic_path = publisher.topic_path(project_id, topic_id)
subscription_path = subscriber.subscription_path(project_id, subscription_id)

# Create Topic
try:
    publisher.create_topic(request={"name": topic_path})
    print("✅ Topic created")
except Exception as e:
    print("Topic exists:", e)

# Create Subscription
try:
    subscriber.create_subscription(
        request={
            "name": subscription_path,
            "topic": topic_path,
        }
    )
    print("✅ Subscription created")
except Exception as e:
    print("Subscription exists:", e)
