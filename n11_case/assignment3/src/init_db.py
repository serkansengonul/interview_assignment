import psycopg2
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

"""
This module is designed to set up a connection to a PostgreSQL database and create necessary tables for an e-commerce application.

Attributes:
    db_name (str): Name of the database.
    db_user (str): User for the database.
    db_password (str): Password for the database user.
    db_host (str): Host of the database.
    db_port (str): Port of the database.
"""

# Database connection details
db_name = "n11db"
db_user = "user"
db_password = "password"
db_host = "db"
db_port = "5432"

# Connect to the database
try:
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
    cursor = conn.cursor()
    logging.info("Successfully connected to the database.")
except Exception as e:
    logging.error(f"Error connecting to the database: {e}")
    raise

# Create Sellers table
try:
    cursor.execute("""
    CREATE TABLE Sellers (
        sellerID VARCHAR(255),
        categoryID VARCHAR(255) NOT NULL
    )
    """)
    logging.info("Sellers table created successfully.")
except Exception as e:
    logging.error(f"Error creating Sellers table: {e}")

# Create Orders table
try:
    cursor.execute("""
    CREATE TABLE Orders (
        orderID VARCHAR(255),
        itemIDs TEXT NOT NULL,
        categoryIDs TEXT NOT NULL,
        sellerIDs TEXT NOT NULL,
        orderstatus VARCHAR(255) CHECK(orderstatus IN ('SUCCESS', 'INVALID')),
        price double precision NOT NULL
    )
    """)
    logging.info("Orders table created successfully.")
except Exception as e:
    logging.error(f"Error creating Orders table: {e}")

# Commit the changes and close the connection
try:
    conn.commit()
    cursor.close()
    conn.close()
    logging.info("Database changes committed and connection closed successfully.")
except Exception as e:
    logging.error(f"Error committing changes or closing the connection: {e}")
