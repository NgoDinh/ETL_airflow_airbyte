This folder contain all step of ETL process:
- Extract and load data by airbyte. Script to trigger airbyte have prefix "airbyte" and locate in dags folder.
- Transform data, it have two wait:
    - using DBT (data build tool): code locate in dbt_transform_postgres folder.
    - using sqlOperator (module of airflow): script can file in sql folder.
- Verify and check quality of data, can find example in dag with script which file have name start with ge_ (if following letter is t, its mean this script using to test data after "T"ransform step. In case "e" you can know it verify "extract" step)