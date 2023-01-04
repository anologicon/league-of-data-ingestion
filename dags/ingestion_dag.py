import datetime
import pendulum
from airflow import models
from airflow.operators.dummy import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.decorators import dag, task
from data_colector.service.api.api_service import APIService
from data_colector.repository.league_of_legends_repository import LeagueOfLegendsRepository
from repository.data_writer.minio_writer import MinioWriter
from data_colector.service.base_request_service import BaseRequestService

api_service = APIService(
    LeagueOfLegendsRepository(BaseRequestService()), 100, 50
)
writer = MinioWriter("league-of-data-raw")

@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False
)
def data_ingestion():     
    
    @task()
    def extract_summoners():
        return api_service.fetch_summoner_data(limit=200)

    @task()
    def fetch_mastery(summoner_list):
        api_service.fetch_summoner_mastery(summoner_list, writer)
        
    @task()
    def fetch_match_id_data(summoner_list):
        return api_service.fetch_summoner_match(summoner_list, writer, 100)
    
    @task()
    def fetch_match_detail(summoner_list_with_match_id):
        api_service.fetch_match_detail(summoner_list_with_match_id, writer)
        
    @task()
    def fetch_match_timeline(summoner_list_with_match_id):
        api_service.fetch_match_timeline(summoner_list_with_match_id, writer)
    
    summooner_details_to_parquet = SparkSubmitOperator(
        task_id='summoner_details_to_parquet', 
        conn_id='spark',
        application="./dags/spark/to_parquet.py",
        packages="com.amazonaws:aws-java-sdk:1.11.563,com.amazonaws:aws-java-sdk-bundle:1.11.874,org.apache.hadoop:hadoop-aws:3.3.2",
        conf={
            "spark.hadoop.fs.s3a.multipart.size": "838860800",
            "spark.hadoop.fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
            "spark.hadoop.fs.s3a.path.style.access": True
        }
    )
    
    
    summoner_list = extract_summoners()
    _, summoner_with_match_list = [fetch_mastery(summoner_list), fetch_match_id_data(summoner_list)]
    [fetch_match_detail(summoner_with_match_list), fetch_match_timeline(summoner_with_match_list)] >> summooner_details_to_parquet  
    
data_ingestion()