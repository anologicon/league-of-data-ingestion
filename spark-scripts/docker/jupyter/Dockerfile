FROM jupyter/base-notebook

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-11-jre

RUN pip install pyspark==3.3.0
RUN pip install delta-spark