import json
import random
import time
import logging
from datetime import datetime
from kafka import KafkaProducer

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a Kafka producer instance with desired configurations.
# Using a value serializer that will convert our dict events to JSON strings
producer = KafkaProducer(bootstrap_servers='kafka:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))


def generate_random_event():
    """
    Generate a random event simulating user interactions with products.

    Returns:
        dict: Randomly generated event.
    """
    product_ids = [f"P{str(i).zfill(5)}" for i in range(10000)]
    event_names = ["productview", "purchase", "addtobasket", "removefrombasket"]
    user_ids = [f"U{str(i).zfill(5)}" for i in range(10000)]

    event = {
        "date": datetime.utcnow().isoformat() + "Z",
        "productId": random.choice(product_ids),
        "eventName": random.choice(event_names),
        "userId": random.choice(user_ids)
    }

    return event


def send_event_to_kafka(event):
    """
    Send a generated event to the Kafka topic.

    Args:
        event (dict): Event data to be sent.
    """
    # Send the event to the "clickstream_events" topic
    producer.send('clickstream_events', event)
    logger.info(f"Sent event to Kafka topic: {event}")


if __name__ == "__main__":
    logger.info("Starting event generation and sending to Kafka.")
    while True:
        event = generate_random_event()
        send_event_to_kafka(event)
        print(event)
        time.sleep(1)
