{{ config(materialized='table') }}
SELECT id, _id, age, name
-- , _airbyte_ab_id, _airbyte_emitted_at, _airbyte_normalized_at, _airbyte_mongotrial_airbyte_user_hashid
	FROM public.mongotrial_airbyte_user