from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os

spark = SparkSession(SparkContext(conf=SparkConf()).getOrCreate())
spark.sparkContext.setLogLevel("ERROR")
sc = spark
hadoop_conf = sc._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
hadoop_conf.set("fs.s3a.endpoint", os.environ["MINIO_URL"])
hadoop_conf.set("fs.s3a.access.key", "minio-root-user")
hadoop_conf.set("fs.s3a.secret.key", "minio-root-password")
hadoop_conf.set("fs.s3a.path.style.access", "True")

summoners_df = spark.read\
                    .option("inferSchema", "true")\
                    .option("header", "true") \
                    .json("s3a://league-of-data-bronze/summoners/details")


summoner_detail = summoners_df.select(
    col("summoner_detail.accountId")
    ,col("summoner_detail.puuid")
    ,col("summoner_detail.profileiconId")
    ,col("summoner_detail.revisionDate")
    ,col("summoner_detail.summonerLevel")
    ,col("summoner_data.*")
    ,col("extracted_at")
)

summoner_detail.createOrReplaceTempView('summer_bronze_temp')

summer_details_duplicates = spark.sql("""
    WITH bronze AS (                                  
        SELECT 
            *
            ,NOW() as ingested_at
            ,ROW_NUMBER() OVER (PARTITION BY accountId ORDER BY extracted_at DESC) as row_number
        FROM summer_bronze_temp
    )
    SELECT * FROM bronze WHERE row_number = 1
""")

summer_details_duplicates = summer_details_duplicates.drop('row_number')

summer_details_duplicates.createTempView('summer_bronze_deduplicate_temp')

dont_exists = True

try:
    summer_details_silver = spark.read.format('delta').load("s3a://league-of-data-silver/summoner/detail/")
except Exception as e:
    dont_exists = False


if dont_exists:
    summer_details_silver.createOrReplaceTempView('summer_details_silver')
    upsert_data = spark.sql("""
        WITH silver AS (
            SELECT 
                *
                ,ROW_NUMBER() OVER (PARTITION BY accountId ORDER BY extracted_at DESC) as row_number
            FROM summer_details_silver
        ), silver_deduplicate AS (
            SELECT * FROM silver WHERE row_number = 1
        )
        SELECT new_data.* FROM silver_deduplicate AS old 
        LEFT JOIN summer_bronze_deduplicate_temp as new_data ON new_data.summonerId = old.summonerId
        WHERE new_data.summonerId IS NULL OR ((new_data.wins + new_data.losses) > (old.wins + old.losses))
    """)
    print(f'New or update summers {upsert_data.count()}')
    upsert_data.write.mode("append").partitionBy("puuid").format(
        "delta"
    ).save("s3a://league-of-data-silver/summoner/detail/")
else:
    summer_details_duplicates.write.mode("overwrite").partitionBy("puuid").format(
        "delta"
    ).save("s3a://league-of-data-silver/summoner/detail/")