import logging
import threading
import json
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from kafka import KafkaConsumer, KafkaProducer

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask application for real-time dashboard
app = Flask(__name__)

# Initialize Socket.io for real-time communication between the server and clients
socketio = SocketIO(app, cors_allowed_origins="*")

# Global dictionary to store real-time event statistics
statistics = {
    'productviewCount': 0,
    'purchaseCount': 0,
    'addtobasketCount': 0,
    'removefrombasketCount': 0
}

# Kafka configuration settings
KAFKA_BROKER_URL = 'kafka:9092'
EVENTS_TOPIC = 'events'
STATS_TOPIC = 'event_statistics'

# Initialize Kafka producer and consumer
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))
consumer = KafkaConsumer(STATS_TOPIC, bootstrap_servers=KAFKA_BROKER_URL,
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')))


@app.route('/')
def index():
    """Endpoint to serve the dashboard page."""
    logger.info("Rendering the dashboard page.")
    return render_template('dashboard.html')


@socketio.on('connect')
def send_current_stats():
    """Socket.io event triggered when a new client connects. Sends current statistics to the client."""
    logger.info("New client connected. Sending current statistics.")
    emit('update_stats', statistics)


def kafka_consumer_thread():
    """Background thread that listens for Kafka messages and updates the statistics."""
    logger.info("Started listening for Kafka messages.")
    for message in consumer:
        data = message.value
        statistics.update(data)
        socketio.emit('update_stats', data)
        logger.info(f"Received data from Kafka and updated statistics: {data}")


if __name__ == '__main__':
    logger.info("Starting the dashboard application.")
    # Start the Kafka consumer thread
    thread = threading.Thread(target=kafka_consumer_thread)
    thread.start()
    # Start the Flask app with Socket.io
    socketio.run(app, host='0.0.0.0', port=5002)
