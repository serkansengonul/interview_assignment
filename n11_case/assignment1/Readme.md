
# Data Pipeline Project

This project aims to create a data pipeline that transfers data from Oracle to BigQuery, constructs the `Potansiyel_Kupon_Maliyeti` and `Kupon_Kullanim` tables, and schedules these tasks using Apache Airflow.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Docker Deployment](#docker-deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Data Transfer**: Transfers specified tables from an Oracle database to Google BigQuery.
- **Data Processing**: Processes the transferred data to create the necessary tables.
- **Scheduling**: Uses Apache Airflow to schedule the data pipeline tasks.

## Requirements

- Python 3.8+
- Oracle Database
- Google BigQuery
- Apache Airflow
- Docker (for Docker deployment)

## Setup & Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/datapipelineproject.git
    cd datapipelineproject
    ```

2. **Install Dependencies**

    Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. **Environment Variables**

    Make sure to set up the necessary environment variables or replace placeholders in the scripts, such as `YOUR_ORACLE_CONNECTION_STRING`, `YOUR_SERVICE_ACCOUNT_JSON`, and `YOUR_PROJECT_ID`.

## Usage

1. **Data Transfer**

    Run the `transfer_source_tables.py` script:

    ```bash
    python transfer_source_tables.py
    ```

2. **Data Processing**

    For processing coupon data:

    ```bash
    python coupon_data_processor.py
    ```

    For processing coupon usage data:

    ```bash
    python coupon_usage_processor.py
    ```

3. **Scheduling with Airflow**

    Make sure Airflow is set up correctly. Place the `create_source_and_target_table_scheduler.py` in the appropriate dags folder of your Airflow setup. The DAG is scheduled to run daily at 03:15 AM.

## Docker Deployment

1. **Build the Docker Image**

    ```bash
    docker build -t datapipelineproject .
    ```

2. **Run the Docker Container**

    ```bash
    docker run datapipelineproject
    ```

## Contributing

Contributions are always welcome! Please read the [contribution guidelines](CONTRIBUTING.md) first.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


additional_content = """
## Note

This README and the associated scripts are samples. Before deploying to your Google Cloud Platform environment:
- Ensure all connection strings, service account paths, and other environment-specific variables are correctly set up for your environment.
- If using the Airflow DAGs, make sure to activate and schedule them in your Airflow environment.
"""

## Manual or Airflow Execution

- **Manual Execution**: If you wish to trigger the pipeline manually, you can run the respective Python files directly.
- **Airflow Execution**: If you prefer to trigger it using Airflow, the `create_source_and_target_table_scheduler.py` file contains the necessary DAG. You should add this DAG to your Airflow setup on Google Cloud Platform.
"""
