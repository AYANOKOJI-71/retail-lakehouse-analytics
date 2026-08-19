FROM apache/airflow:2.10.4-python3.12

USER root
COPY pyproject.toml /opt/airflow/lakehouse/pyproject.toml
COPY src /opt/airflow/lakehouse/src
RUN chown -R airflow:root /opt/airflow/lakehouse

USER airflow
RUN pip install --no-cache-dir /opt/airflow/lakehouse
