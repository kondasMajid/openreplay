from datetime import datetime, timedelta
from textwrap import dedent

import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import os
_work_dir = os.getcwd()

def my_function():
    l = os.listdir('scripts')
    print(l)
    return l

dag = DAG(
    "first_test",
    default_args={
        "depends_on_past": True,
        "retries": 1,
        "retry_delay": timedelta(minutes=3),
    },
    start_date=pendulum.datetime(2015, 12, 1, tz="UTC"),
    description="My first test",
    schedule="@daily",
    catchup=False,
)


#assigning the task for our dag to do
with dag:
    first_world = PythonOperator(
        task_id='FirstTest',
        python_callable=my_function,
    )
    hello_world = BashOperator(
        task_id='OneTest',
        bash_command=f'python {_work_dir}/scripts/task.py --mode train --kernel linear',
        # provide_context=True
    )
    first_world >> hello_world
