from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql.functions import regexp_extract
from functools import partial

spark = (
    SparkSession.builder.appName("ToParquetLeagueOfData")
    .master("spark://localhost:7077")
    .config(
        "spark.jars.packages",
        "com.amazonaws:aws-java-sdk:1.11.563,com.amazonaws:aws-java-sdk-bundle:1.11.874,org.apache.hadoop:hadoop-aws:3.3.2",
    )
    .config("spark.hadoop.fs.s3a.multipart.size", "838860800")
    .config(
        "spark.hadoop.fs.s3a.aws.credentials.provider",
        "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
    )
    .config("spark.hadoop.fs.s3a.path.style.access", True)
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")
sc = spark
hadoop_conf = sc._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
hadoop_conf.set("fs.s3a.endpoint", "http://192.168.0.10:9000")
hadoop_conf.set("fs.s3a.access.key", "OhLfedtD1ulumaig")
hadoop_conf.set("fs.s3a.secret.key", "IuWsU1j3YvArUAS26VDOvRPnLYLWUXBo")
hadoop_conf.set("fs.s3a.path.style.access", "True")

summoners_df = spark.read.json("s3a://league-of-data-raw/")
