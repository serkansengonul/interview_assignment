import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from collections import defaultdict
from datetime import datetime

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to the Kafka server
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def consume_events_from_kafka(topic_name):
    """Connect to Kafka and consume events from the specified topic."""
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers='kafka:9092',
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        group_id='event-consumer-group'
    )
    return consumer


def calculate_event_statistics(events):
    """Calculate event statistics from the list of events."""
    event_counts = defaultdict(int)

    for event in events:
        event_name = event['eventName']
        event_counts[event_name] += 1

    return event_counts


def send_statistics_to_kafka(stats):
    """Send the calculated statistics to the Kafka topic."""
    stats['receivedAt'] = datetime.utcnow().isoformat() + "Z"
    producer.send('event_statistics', stats)
    logger.info(f"Sent statistics to Kafka: {stats}")


if __name__ == "__main__":
    logger.info("Starting the event consumer.")
    consumer = consume_events_from_kafka('clickstream_events')
    batch_size = 100
    events_batch = []

    for message in consumer:
        event = message.value
        logger.debug(f"Received event: {event}")
        events_batch.append(event)

        # Process events in batches to optimize the calculation
        if len(events_batch) >= batch_size:
            stats = calculate_event_statistics(events_batch)
            send_statistics_to_kafka(stats)
            events_batch.clear()

