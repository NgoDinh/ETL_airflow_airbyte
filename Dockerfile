FROM apache/airflow:2.5.1
# ${AIRFLOW_IMAGE_NAME}:-apache/airflow:2.5.1

USER airflow
RUN echo "123123456789034567"
RUN pip install apache-airflow-providers-airbyte[http] \
&& pip install apache-airflow-providers-airbyte\
&& pip install dbt-postgres\
&& dbt init dbt_transform_postgres -s
RUN echo "=============================================="
COPY profiles.yml /home/airflow/.dbt/profiles.yml
