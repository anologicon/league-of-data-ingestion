import datetime
from airflow import models
from airflow.operators.dummy import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.decorators import dag, task
from data_colector.service.api.api_service import APIService
from data_colector.repository.league_of_legends_repository import LeagueOfLegendsRepository
from data_colector.service.base_request_service import BaseRequestService

api_service = APIService(
    LeagueOfLegendsRepository(BaseRequestService()), 10, 5
)
writer = MinioWriter("league-of-data-raw")

with models.DAG(dag_id="data_lol_batch",
                start_date=datetime.datetime(2022, 2, 2),
                schedule_interval="0 */1 * * *",
                default_args={
                        "owner": "BI",
                        "email_on_failure": False,
                },
                catchup=False, ) as dag:

     
    @task
    def extract_summoners():
        summoners_data_list = api_service.fetch_summoner_data(limit=200)