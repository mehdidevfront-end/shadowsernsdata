from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def generate_pdf(**context):
    # call the reporting script in repo
    import subprocess
    subprocess.check_call(['python3', '/opt/airflow/dags/scripts/generate_pdf_report.py'])


with DAG(
    dag_id='weekly_pdf_report',
    default_args=default_args,
    description='Generate weekly PDF report and store it (MinIO)',
    schedule_interval='0 6 * * 1',  # every Monday 06:00
    start_date=datetime(2025, 11, 1),
    catchup=False,
) as dag:

    task_generate = PythonOperator(
        task_id='generate_pdf',
        python_callable=generate_pdf,
        provide_context=True,
    )

    task_generate
