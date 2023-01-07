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
    "spark.hadoop.fs.s3a.path.style.access": True,
}


@dag(schedule=None, start_date=pendulum.datetime(2023, 1, 1, tz="UTC"), catchup=False)
def spark_gold_etl():

    summoner_details = SparkSubmitOperator(
        task_id="summoner_details",
        conn_id="spark",
        application="./dags/spark/gold_summoner.py",
        packages=PACKAGES,
        conf=CONFIG,
        name="SummonerDetails",
        retries=2,
    )

    summoner_matches = SparkSubmitOperator(
        task_id="summoner_matches",
        conn_id="spark",
        application="./dags/spark/gold_match.py",
        packages=PACKAGES,
        conf=CONFIG,
        name="SummonerMatchesData",
        retries=2,
    )
    
    to_dw = SparkSubmitOperator(
        task_id="to_dw",
        conn_id="spark",
        application="./dags/spark/to_postgress.py",
        packages=PACKAGES+",org.postgresql:postgresql:42.2.18",
        conf=CONFIG,
        name="ToDataWareHouse",
        retries=2,
    )

    dummy = DummyOperator(task_id="dummy_start")

    dummy >> [summoner_details, summoner_matches] >> to_dw


spark_gold_etl()
