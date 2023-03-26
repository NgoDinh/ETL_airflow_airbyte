import airflow
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from ruamel import yaml
import great_expectations as gx
from great_expectations.core.batch import BatchRequest, RuntimeBatchRequest
from great_expectations.cli.datasource import sanitize_yaml_and_save_datasource, check_if_datasource_name_exists

# from my_script import my_python_function
def set_up_source():
    context = gx.get_context()
    datasource_name = "postgres_aws_1"
    host = "13.229.110.215"
    port = "5432"
    username = "vu_ngo"
    password = "1993"
    database = "vu_ngo"
    schema_name = "public"

    # A table that you would like to add initially as a Data Asset
    table_name = "fact_user"

    example_yaml = f"""
    name: {datasource_name}
    class_name: Datasource
    execution_engine:
      class_name: SqlAlchemyExecutionEngine
      credentials:
        host: {host}
        port: '{port}'
        username: {username}
        password: {password}
        database: {database}
        drivername: postgresql
    data_connectors:
      default_runtime_data_connector_name:
        class_name: RuntimeDataConnector
        batch_identifiers:
          - default_identifier_name
      default_inferred_data_connector_name:
        class_name: InferredAssetSqlDataConnector
        include_schema_name: True
        introspection_directives:
          schema_name: {schema_name}
      default_configured_data_connector_name:
        class_name: ConfiguredAssetSqlDataConnector
        assets:
          {table_name}:
            class_name: Asset
            schema_name: {schema_name}
    """

    # print(context.test_yaml_config(yaml_config=example_yaml))
    sanitize_yaml_and_save_datasource(context, example_yaml, overwrite_existing=True)
    print(context.list_datasources())

def ge_t_postgres_fact_user():
    context = gx.get_context()
    batch_request = RuntimeBatchRequest(
        datasource_name="postgres_aws_1",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name="default_name",  # this can be anything that identifies this data
        runtime_parameters={"query": "SELECT * FROM public.fact_user"},
        batch_identifiers={"default_identifier_name": "default_identifier"},
    )

    validator = context.get_validator(batch_request=batch_request)
    validator.expect_column_values_to_not_be_null("id")
    validator.expect_column_values_to_not_be_null("age")
    validator.expect_column_values_to_not_be_null("name")

    checkpoint = gx.checkpoint.SimpleCheckpoint( 
        name="my_quickstart_checkpoint",
        data_context=context,
        validator=validator,
    )
    checkpoint_result = checkpoint.run()
    result = dict(list(checkpoint_result.values())[2])
    fail_count = result[list(result.keys())[0]]['validation_result']['statistics']['unsuccessful_expectations']
    if fail_count > 0:
        print("-----------------Fail-------------------")
        # print(result[list(result.keys())[0]]['validation_result'])
        for details in result[list(result.keys())[0]]['validation_result']['results']:
            if details["success"] == False:
                print(details['expectation_config'])
    else:
        print("-----------------Success-------------------")
        
# ge_t_postgres_fact_user()

#################################################################


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG('ge_t_postgres_fact_user', default_args=default_args)

t1 = PythonOperator(dag=dag,
               task_id='set_up_source',
               python_callable=set_up_source,
               )

t2 = PythonOperator(dag=dag,
               task_id='ge_t_postgres_fact_user',
               python_callable=ge_t_postgres_fact_user,
               )

t1 >> t2