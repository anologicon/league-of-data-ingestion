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

matchs_df = spark.read.format("delta").load("s3a://league-of-data-gold/matchs")

matchs_game_creation_df = (
    matchs_df.withColumn(
        "gameCreation",
        F.from_unixtime(matchs_df.gameCreation / 1000, "yyyy-MM-dd HH:mm:ss"),
    )
    .withColumn(
        "gameEndTimestamp",
        F.from_unixtime(matchs_df.gameEndTimestamp / 1000, "yyyy-MM-dd HH:mm:ss"),
    )
    .withColumn(
        "gameStartTimestamp",
        F.from_unixtime(matchs_df.gameStartTimestamp / 1000, "yyyy-MM-dd HH:mm:ss"),
    )
    .withColumn("gameDuration", matchs_df.gameDuration / 60)
)

matchs_game_creation_df.write.mode("overwrite").format("jdbc").option(
    "url", "jdbc:postgresql://data_warehouse:5432/data_lol_dw"
).option("driver", "org.postgresql.Driver").option("dbtable", "match_detail").option(
    "user", "data_lol"
).option(
    "password", "data_lol"
).save()

summoner_df = spark.read.format("delta").load(
    "s3a://league-of-data-gold/summoner/detail"
)

summoner_df.write.mode("overwrite").format("jdbc").option(
    "url", "jdbc:postgresql://data_warehouse:5432/data_lol_dw"
).option("driver", "org.postgresql.Driver").option("dbtable", "summoner_detail").option(
    "user", "data_lol"
).option(
    "password", "data_lol"
).save()
