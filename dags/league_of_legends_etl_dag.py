import pendulum
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.docker.operators.docker import DockerOperator
import os


@dag(schedule=None, start_date=pendulum.datetime(2023, 1, 1, tz="UTC"), catchup=False)
def league_of_legends_etl():
    docker_etl = DockerOperator(
        task_id='data-collector',
        image='anologicon/lodi-data-collector:v1',
        force_pull=True,
        command='python main.py -l 10 -mm 10',
        network_mode='lol-data',
        environment={
            'MINIO_URL': os.environ['MINIO_URL'],
            'LOL_API_KEY': os.environ['LOL_API_KEY']
        },
        docker_url='tcp://docker-proxy:2375',
        api_version='auto',
        mount_tmp_dir=False
    )

    docker_static = DockerOperator(
        task_id='data-static',
        image='anologicon/lodi-data-collector:v1',
        force_pull=True,
        command='python static_files.py',
        network_mode='lol-data',
        docker_url='tcp://docker-proxy:2375',
        environment={
            'MINIO_URL': os.environ['MINIO_URL']
        },
        api_version='auto',
        mount_tmp_dir=False
    )

    spark_jobs_dag = TriggerDagRunOperator(
        task_id="trigger_spark_etl", trigger_dag_id="spark_silver_etl"
    )

    dummy = EmptyOperator(task_id="dummy_start")

    dummy >> [docker_etl, docker_static] >> spark_jobs_dag


league_of_legends_etl()
