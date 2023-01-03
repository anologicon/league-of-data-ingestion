FROM apache/airflow:2.5.0

USER root

RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-11-jre

# Prints installed java version, just for checking
RUN java --version
ENV PYTHONPATH=${PYTHONPATH}:/opt/airflow/data_colector

USER airflow
RUN python -m pip install --upgrade pip
RUN pip install apache-airflow-providers-apache-spark==3.0.0