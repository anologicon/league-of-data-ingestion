from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql.functions import regexp_extract
from functools import partial
import os

spark = SparkSession.builder.getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
sc = spark
hadoop_conf = sc._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
hadoop_conf.set("fs.s3a.endpoint", os.environ["MINIO_URL"])
hadoop_conf.set("fs.s3a.access.key", "minio-root-user")
hadoop_conf.set("fs.s3a.secret.key", "minio-root-password")
hadoop_conf.set("fs.s3a.path.style.access", "True")

summoners_df = spark.read.json("s3a://league-of-data-bronze/summoners/details")
summone_detail = summoners_df.select(
    col("summoner_detail.*"), col("summoner_data.*"), col("extracted_at")
)
summone_detail.write.mode("overwrite").partitionBy("puuid", "extracted_at").format(
    "delta"
).save("s3a://league-of-data-silver/summoner/detail/")
