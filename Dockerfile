FROM apache/airflow:2.5.1
# ${AIRFLOW_IMAGE_NAME}:-apache/airflow:2.5.1
USER root
RUN apt-get -y update && apt-get install -y libzbar-dev

USER airflow
RUN echo "=========set up GE=================="
RUN pip install great_expectations
RUN echo y| great_expectations init
RUN echo "=========set up dependencies=================="
RUN pip install sqlalchemy psycopg2-binary
RUN echo "=========set up airbyte=================="
RUN pip install apache-airflow-providers-airbyte[http] \
&& pip install apache-airflow-providers-airbyte
RUN echo "=========set up dbt=================="
RUN pip install dbt-postgres\
&& dbt init dbt_transform_postgres -s
COPY prefill_dbt_profiles.yml /home/airflow/.dbt/profiles.yml
# COPY prefill_GE.yml /home/airflow/great_expectations/great_expectations.yml
# RUN chown -R /home/airflow/great_expectations
# docker exec -u 0 -it 07b54bb2b8deef203a07a9f6613c5bda7dca14beebe124dafb66d5963f7adafe bash
# find ~/ -type f -name "great_expectations.yml"
