from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

# allow import from your project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from ingestion.pipeline import run_pipeline


def run_etl():
    run_pipeline("data/raw/customers.csv")


with DAG(
    dag_id="etl_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id="run_etl",
        python_callable=run_etl
    )

    task1
