import datetime
import pendulum
from airflow import models
from airflow.operators.dummy import DummyOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.decorators import dag, task
from data_colector.service.api.api_service import APIService
from data_colector.repository.league_of_legends_repository import LeagueOfLegendsRepository
from repository.data_writer.minio_writer import MinioWriter
from data_colector.service.base_request_service import BaseRequestService

api_service = APIService(
    LeagueOfLegendsRepository(BaseRequestService()), 10, 5
)
writer = MinioWriter("league-of-data-raw")

@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False
)
def league_of_legends_etl():     
    
    @task()
    def extract_summoners():
        return api_service.fetch_summoner_data(limit=5)

    @task()
    def fetch_mastery(summoner_list):
        api_service.fetch_summoner_mastery(summoner_list, writer)
        
    @task()
    def fetch_match_id_data(summoner_list):
        return api_service.fetch_summoner_match(summoner_list, writer, 10)
    
    @task()
    def fetch_match_detail(summoner_list_with_match_id):
        api_service.fetch_match_detail(summoner_list_with_match_id, writer)
        
    @task()
    def fetch_match_timeline(summoner_list_with_match_id):
        api_service.fetch_match_timeline(summoner_list_with_match_id, writer)
    
    spark_jobs_dag = TriggerDagRunOperator(
        task_id='trigger_spark_etl',
        trigger_dag_id='spark_bronze_etl'
    )
    
    
    summoner_list = extract_summoners()
    _, summoner_with_match_list = [fetch_mastery(summoner_list), fetch_match_id_data(summoner_list)]
    [fetch_match_detail(summoner_with_match_list), fetch_match_timeline(summoner_with_match_list)] >> spark_jobs_dag  
    
league_of_legends_etl()