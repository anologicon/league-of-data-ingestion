from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql.functions import regexp_extract
from functools import partial

spark = (
    SparkSession.builder.appName("ToParquetLeagueOfData")
    .master("spark://spark-master:7077")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")
sc = spark
hadoop_conf = sc._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
hadoop_conf.set("fs.s3a.endpoint", "http://minio:9000")
hadoop_conf.set("fs.s3a.access.key", "OhLfedtD1ulumaig")  # keys geradas no painel do minio
hadoop_conf.set("fs.s3a.secret.key", "IuWsU1j3YvArUAS26VDOvRPnLYLWUXBo") # keys geradas no painel do minio
hadoop_conf.set("fs.s3a.path.style.access", "True")

summoners_df = spark.read.json("s3a://league-of-data-bronze/")
details = summoners_df.select("summoner_detail")

details.write.parquet("s3a://league-of-data-bronze/silver/details.parquet")
