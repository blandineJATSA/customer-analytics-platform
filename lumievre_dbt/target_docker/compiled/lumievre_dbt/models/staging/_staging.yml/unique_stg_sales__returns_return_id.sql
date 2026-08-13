
    
    

with dbt_test__target as (

  select return_id as unique_field
  from `starlit-gift-504722-c7`.`lumievre_staging`.`stg_sales__returns`
  where return_id is not null

)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1


