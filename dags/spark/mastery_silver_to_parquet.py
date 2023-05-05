from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark import SparkConf, SparkContext
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

mastery_df = spark.read.json("s3a://league-of-data-bronze/summoners/mastery")
summoners_df = spark.read.json("s3a://league-of-data-bronze/summoners/details")
summoners_id_df = summoners_df.select(
    col("summoner_detail.id")
).distinct()
mastery_puuid_df = mastery_df.join(
    summoners_id_df, mastery_df.summonerId == summoners_id_df.id
)
mastery_puuid_df.write.mode("overwrite").partitionBy("puuid", "extracted_at").format(
    "delta"
).save("s3a://league-of-data-silver/summoner/mastery/")
