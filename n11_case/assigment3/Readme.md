
# E-Commerce Data Service

This project sets up a Flask web service designed for an e-commerce platform. It leverages a PostgreSQL database to store and retrieve seller and order data.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Ensure you have Docker and Docker Compose installed on your system.
- Clone the project to your local machine.

### Installation

1. Clone the project repository:
```bash
git clone [repository-url]
```

2. Navigate to the project directory:
```bash
cd [directory-name]
```

3. Use Docker Compose to build and start the services:
```bash
docker-compose up --build
```

## Features

- **Database Setup**: Initializes the PostgreSQL database with tables for sellers and orders.
- **ETL Process**: Extracts data from JSON files and loads them into the PostgreSQL database.
- **API Endpoint**: Provides an endpoint to retrieve the top 5 sellers based on Gross Merchandise Value (GMV) for a specific category.

## Usage

Once the services are up, you can access the Flask web service by navigating to:
```
http://localhost:1234/top_sellers?cat=[category-id]
```
Replace `[category-id]` with the desired category ID to retrieve the top 5 sellers for that category.

## Built With

- **Flask**: Lightweight web application framework.
- **PostgreSQL**: Open-source relational database.
- **Docker**: Used for containerization and ensuring consistent environments.

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcomed.

## License

This project is licensed under the MIT License. See `LICENSE.md` for details.

## Acknowledgments

- Thanks to OpenAI for guidance and code assistance.
