from google.cloud import bigquery
import cx_Oracle
import pandas as pd

"""
Constants:
- ORACLE_CONN_STR: Connection string for Oracle database.
- SERVICE_ACCOUNT_JSON: Path to the Google Cloud service account JSON file.
- PROJECT_ID: Google Cloud project ID.
- DATASET_NAME: Name of the dataset in BigQuery.
- TABLES: List of table names to be transferred from Oracle to BigQuery.
"""
ORACLE_CONN_STR = 'your_oracle_connection_string'
SERVICE_ACCOUNT_JSON = 'path_to_your_service_account_json_file.json'
PROJECT_ID = 'your_project_id'
DATASET_NAME = 'n11_VA_tablolari'
TABLES = ["Kupon_Kullanim", "Urun", "Kupon_Kullanim_Kriteri", "Kategori_Cizelge", "Kuponlar", "Siparis_Kalemleri"]

def oracle_to_bigquery_transfer():
    """
    This function is responsible for:
    1. Establishing a connection with the Oracle database.
    2. Creating a BigQuery client instance.
    3. Iterating over the list of tables and:
       a. Fetching the data from Oracle using pandas.
       b. Uploading the data to BigQuery.
    """
    # Establish connection to Oracle
    with cx_Oracle.connect(ORACLE_CONN_STR) as conn:
        # Create BigQuery client
        client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)
        dataset_ref = client.dataset(DATASET_NAME)

        # Transfer each table from Oracle to BigQuery
        for table in TABLES:
            # Fetch data from Oracle
            df = pd.read_sql(f"SELECT * FROM {table}", conn)

            # Upload data to BigQuery
            table_ref = dataset_ref.table(table)
            job = client.load_table_from_dataframe(df, table_ref)
            job.result()
            print(f"Transferred {table} from Oracle to BigQuery successfully!")

if __name__ == "__main__":
    """
    The entry point of the script.
    If the script is executed as the main program, it will call the oracle_to_bigquery_transfer function.
    """
    oracle_to_bigquery_transfer()
