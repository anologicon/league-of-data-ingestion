FROM bde2020/spark-master:3.3.0-hadoop3.3

USER root

RUN wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.11.563/aws-java-sdk-1.11.563.jar -P /spark/jars 
RUN wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-s3/1.12.368/aws-java-sdk-s3-1.12.368.jar -P /spark/jars 
RUN wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.874/aws-java-sdk-bundle-1.11.874.jar -P /spark/jars
RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.2/hadoop-aws-3.3.2.jar -P /spark/jars

# /spark/bin/spark-submit  /app/to_spark.py
