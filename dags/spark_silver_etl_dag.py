import datetime
import pendulum
from airflow import models
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.decorators import dag, task
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

PACKAGES = "com.amazonaws:aws-java-sdk:1.11.563,com.amazonaws:aws-java-sdk-bundle:1.11.874,org.apache.hadoop:hadoop-aws:3.3.2,io.delta:delta-core_2.12:2.1.0"
CONFIG = {
    "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
    "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    "spark.hadoop.fs.s3a.multipart.size": "838860800",
    "spark.hadoop.fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
    "spark.hadoop.fs.s3a.path.style.access": True,
}


@dag(schedule=None, start_date=pendulum.datetime(2023, 1, 1, tz="UTC"), catchup=False)
def spark_silver_etl():

    summoner_details_to_parquet = SparkSubmitOperator(
        task_id="summoner_details_to_parquet",
        conn_id="spark",
        application="./dags/spark/summoner_details_silver_to_parquet.py",
        packages=PACKAGES,
        conf=CONFIG,
        name="SummonerDetailsDataToBronze",
        retries=2,
    )

    summoner_matches_to_parquet = SparkSubmitOperator(
        task_id="summoner_matches_to_parquet",
        conn_id="spark",
        application="./dags/spark/summoner_matches_silver_to_parquet.py",
        packages=PACKAGES,
        conf=CONFIG,
        name="SummonerMatchesDataToBronze",
        retries=2,
    )

    matches_to_parquet = SparkSubmitOperator(
        task_id="matches_to_parquet",
        conn_id="spark",
        application="./dags/spark/matches_silver_to_parquet.py",
        packages=PACKAGES,
        conf=CONFIG,
        name="MatchesDataToBronze",
        retries=2,
    )

    mastery_silver_to_parquet = SparkSubmitOperator(
        task_id="mastery_silver_to_parquet",
        conn_id="spark",
        application="./dags/spark/mastery_silver_to_parquet.py",
        packages=PACKAGES,
        conf=CONFIG,
        name="MatchesDataToBronze",
        retries=2,
    )

    spark_gold_jobs_dag = TriggerDagRunOperator(
        task_id="trigger_gold_spark_etl", trigger_dag_id="spark_gold_etl"
    )

    dummy = EmptyOperator(task_id="dummy_start")

    (
        dummy
        >> [
            summoner_details_to_parquet,
            summoner_matches_to_parquet,
            matches_to_parquet,
            mastery_silver_to_parquet,
        ]
        >> spark_gold_jobs_dag
    )


spark_silver_etl()
