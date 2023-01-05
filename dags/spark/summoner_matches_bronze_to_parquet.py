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

summoner_details_df = spark.read.json("s3a://league-of-data-raw/summoners/details/")
summoner_matchs_df = summoner_details_df.withColumn("matches", explode(summoner_details_df.matches))
summoner_matchs_row_df = summoner_matchs_df.select(col("matches"), col("summoner_detail.puuid"), col("extracted_at"))
summoner_matchs_row_df.write.mode("overwrite").partitionBy("puuid", "extracted_at").format("delta").save("s3a://league-of-data-bronze/summoner/matches/")
