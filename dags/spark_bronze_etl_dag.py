import datetime
import pendulum
from airflow import models
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.decorators import dag, task

@dag(
    schedule=None,
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False
)
def spark_bronze_etl():     
    
    summooner_details_to_parquet = SparkSubmitOperator(
        task_id='summoner_details_to_parquet', 
        conn_id='spark',
        application="./dags/spark/to_parquet.py",
        packages="com.amazonaws:aws-java-sdk:1.11.563,com.amazonaws:aws-java-sdk-bundle:1.11.874,org.apache.hadoop:hadoop-aws:3.3.2",
        conf={
            "spark.hadoop.fs.s3a.multipart.size": "838860800",
            "spark.hadoop.fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
            "spark.hadoop.fs.s3a.path.style.access": True
        },
        name="RawDataToBronze"
    )
    
    
    summooner_details_to_parquet  
    
spark_bronze_etl()