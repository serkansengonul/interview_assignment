import psycopg2
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

"""
This module is designed to populate the PostgreSQL database tables from JSON files. 
It reads data from 'sellers.json' and 'orders.json' and inserts the records into the respective tables.

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

# Reading data from sellers.json and inserting into Sellers table
try:
    with open("/app/data/sellers.json", "r") as f:
        lines = f.readlines()
        for line in lines:
            data = json.loads(line)
            for seller in data:
                cursor.execute("INSERT INTO Sellers (sellerID, categoryID) VALUES (%s, %s)",
                               (seller["sellerID"], seller["categoryID"]))
    logging.info("Data from sellers.json inserted into Sellers table.")
except Exception as e:
    logging.error(f"Error reading data from sellers.json or inserting into Sellers table: {e}")

# Reading data from orders.json and inserting into Orders table
try:
    with open("/app/data/orders.json", "r") as f:
        lines = f.readlines()
        for line in lines:
            data = json.loads(line)
            for order in data:
                cursor.execute("INSERT INTO Orders (orderID, itemIDs, categoryIDs, sellerIDs, orderstatus, price) VALUES "
                               "(%s, %s, %s, %s, %s, %s)",
                           (order["orderID"], order["itemIDs"], order["categoryIDs"], order["sellerIDs"], order["orderstatus"], order["price"]))
    logging.info("Data from orders.json inserted into Orders table.")
except Exception as e:
    logging.error(f"Error reading data from orders.json or inserting into Orders table: {e}")

# Committing the changes and closing the connection
try:
    conn.commit()
    cursor.close()
    conn.close()
    logging.info("Database changes committed and connection closed successfully.")
except Exception as e:
    logging.error(f"Error committing changes or closing the connection: {e}")
