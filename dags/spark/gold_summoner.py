from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F
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

summoner_detail_df = spark.read.format("delta").load(
    "s3a://league-of-data-silver/summoner/detail"
)
summoner_data_df = summoner_detail_df.drop(
    "summonerId", "summonerName", "profileIconId"
)
summoner_data_unique_df = summoner_data_df.dropDuplicates(["puuid", "extracted_at"])
summoner_data_unique_revision_df = summoner_data_unique_df.withColumn(
    "revisionDate",
    F.from_unixtime(summoner_data_unique_df.revisionDate / 1000, "yyyy-MM-dd HH:mm:ss"),
)
summoner_data_unique_revision_df.write.mode("overwrite").partitionBy("puuid").format(
    "delta"
).save("s3a://league-of-data-gold/summoner/detail/")
