FROM apache/airflow:2.5.1
# ${AIRFLOW_IMAGE_NAME}:-apache/airflow:2.5.1

USER airflow
RUN pip install apache-airflow-providers-airbyte[http] \
&& pip install apache-airflow-providers-airbyte\
# && pip install airflow-provider-great-expectations==0.1.1\
&& pip install dbt-postgres