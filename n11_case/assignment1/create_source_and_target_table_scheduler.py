from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

"""
Define default arguments for the DAG. 
These arguments define the basic configurations for the DAG execution.
"""
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

"""
Define the DAG itself, specifying its ID, description, schedule, and other configurations.
This DAG is designed to transfer data from Oracle to BigQuery and to construct 
`Potansiyel_Kupon_Maliyeti` and `Kupon_Kullanim` tables.
The DAG is scheduled to run daily at 03:15 AM.
"""
dag = DAG(
    'complete_data_pipeline_dag',
    default_args=default_args,
    description='A DAG to transfer data from Oracle to BigQuery, construct Potansiyel_Kupon_Maliyeti and '
                'Kupon_Kullanim tables',
    schedule_interval='15 3 * * *',
    start_date=datetime(2023, 10, 23),
    catchup=False
)

"""
Function to transfer data from source tables.
This function will execute the content of transfer_source_tables.py script.
"""


def transfer_source_tables():
    exec(open("transfer_source_tables.py").read())


"""
Function to construct a table for potential coupon costs.
This function will execute the content of CouponDataProcessor.py script.
"""


def construct_potential_coupon_cost_table():
    exec(open("CouponDataProcessor.py").read())


"""
Function to construct a table for coupon usage.
This function will execute the content of CouponUsageProcessor.py script.
"""


def construct_coupon_usage_table():
    exec(open("CouponUsageProcessor.py").read())


"""
Define individual tasks using PythonOperator. 
Each task corresponds to one of the functions defined above.
"""
t1 = PythonOperator(
    task_id='transfer_source_tables',
    python_callable=transfer_source_tables,
    dag=dag
)

t2 = PythonOperator(
    task_id='construct_potential_coupon_cost_table',
    python_callable=construct_potential_coupon_cost_table,
    dag=dag
)

t3 = PythonOperator(
    task_id='construct_coupon_usage_table',
    python_callable=construct_coupon_usage_table,
    dag=dag
)

"""
Set the order of execution for tasks. 
The data transfer task runs first, followed by the table construction tasks.
"""
t1 >> t2 >> t3
