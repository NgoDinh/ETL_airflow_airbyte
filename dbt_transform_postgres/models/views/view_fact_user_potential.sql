{{ config(materialized='view') }}

select *
from {{ ref('fact_user') }}
where age is not null