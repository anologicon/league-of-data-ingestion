import datetime
import pendulum
from airflow import models
from airflow.operators.dummy import DummyOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.decorators import dag, task


PACKAGES = "com.amazonaws:aws-java-sdk:1.11.563,com.amazonaws:aws-java-sdk-bundle:1.11.874,org.apache.hadoop:hadoop-aws:3.3.2,io.delta:delta-core_2.12:2.1.0"
CONFIG = {
            "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
            "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
            "spark.hadoop.fs.s3a.multipart.size": "838860800",
            "spark.hadoop.fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
            "spark.hadoop.fs.s3a.path.style.access": True
        }
@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False
)
def spark_bronze_etl():     
    
    summoner_details_to_parquet = SparkSubmitOperator(
        task_id='summoner_details_to_parquet', 
        conn_id='spark',
        application="./dags/spark/summoner_details_bronze_to_parquet.py",
        packages=PACKAGES,
        conf=CONFIG,
        name="SummonerDetailsDataToBronze"
    )
    
    summoner_matches_to_parquet = SparkSubmitOperator(
        task_id='summoner_matches_to_parquet', 
        conn_id='spark',
        application="./dags/spark/summoner_matches_bronze_to_parquet.py",
        packages=PACKAGES,
        conf=CONFIG,
        name="SummonerMatchesDataToBronze"
    )
    
    matches_to_parquet = SparkSubmitOperator(
        task_id='matches_to_parquet', 
        conn_id='spark',
        application="./dags/spark/matches_bronze_to_parquet.py",
        packages=PACKAGES,
        conf=CONFIG,
        name="MatchesDataToBronze"
    )
    
    mastery_bronze_to_parquet = SparkSubmitOperator(
        task_id='mastery_bronze_to_parquet', 
        conn_id='spark',
        application="./dags/spark/mastery_bronze_to_parquet.py",
        packages=PACKAGES,
        conf=CONFIG,
        name="MatchesDataToBronze"
    )
    
    dummy = DummyOperator(task_id='dummy_start')
    
    dummy >> [summoner_details_to_parquet, summoner_matches_to_parquet, matches_to_parquet, mastery_bronze_to_parquet]  
    
spark_bronze_etl()