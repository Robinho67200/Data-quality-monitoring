from __future__ import annotations
import datetime
import pendulum
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from pathlib import Path

parent_path = Path(__file__).parent.parent.parent

with DAG(
    dag_id="extract_transform_data",
    schedule="0 20 * * *",
    start_date=pendulum.datetime(2025, 3, 10, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["Data quality monitoring"],
) as dag:
    extract_data = BashOperator(
        task_id="extract_data",
        bash_command=f"python3 {parent_path}/src/request_api.py",
    )

    transform_data = BashOperator(
        task_id="transform_data",
        bash_command=f"python3 {parent_path}/src/reading_data_csv.py",
    )

    extract_data >> transform_data

if __name__ == "__main__":
    dag.test()