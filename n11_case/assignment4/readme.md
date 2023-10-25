
# Real-time Event Dashboard with Kafka, Flask, and Socket.io

This project aims to create a real-time event dashboard using Kafka for event streaming, Flask for the web backend, and Socket.io for real-time updates.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
    - [Running the App with Docker](#running-the-app-with-docker)
3. [Understanding the Code](#understanding-the-code)
4. [Contributing](#contributing)
5. [License](#license)
6. [Acknowledgments](#acknowledgments)

## System Architecture

The system comprises three main components:

- **Producer**: Generates random events, which are then sent to Kafka.
- **Consumer**: Consumes the events from Kafka, calculates statistics, and sends these stats back to another Kafka topic.
- **Dashboard**: A Flask web application that displays the real-time statistics using Socket.io for real-time updates.

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9

### Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

### Running the App with Docker

1. Build the Docker images:

```bash
docker-compose build
```

2. Start the services:

```bash
docker-compose up
```

This command starts all the services defined in the `docker-compose.yml` file. Kafka, Zookeeper, and the main application will be initialized. 

3. Access the dashboard at `http://localhost:5002/`.

Note: The application waits for 30 seconds before starting to ensure that the Kafka service is up and running. This delay is defined in the `docker-compose.yml` file.

4. If you want to shut down the application and remove the containers, networks, and volumes defined in the `docker-compose.yml` file, run:

```bash
docker-compose down
```

## Understanding the Code

- `producer.py`: Simulates event generation for actions like `productview`, `purchase`, `addtobasket`, and `removefrombasket`. These events are then sent to a Kafka topic.
  
- `consumer.py`: Consumes the events, calculates statistics, and sends the aggregated data to another Kafka topic.
  
- `dashboard.py`: A Flask web application that displays the stats. It consumes the aggregated data from Kafka and updates the dashboard in real-time using Socket.io.

- `templates/dashboard.html`: The frontend of the dashboard which uses Socket.io to get real-time updates and display them.

## Contributing

1. Fork the project.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Thanks to Kafka, Flask, and Socket.io communities for their comprehensive documentation and tutorials.
- This project was set up with assistance from the OpenAI team.
