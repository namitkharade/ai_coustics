FROM apache/airflow:2.7.3

USER root
# Install g++ compiler
RUN apt-get update \
    && apt-get install -y g++ \
    && rm -rf /var/lib/apt/lists/*

USER airflow
COPY requirements.txt /
RUN pip install --no-cache-dir "apache-airflow==2.7.3" -r /requirements.txt
