
    
    

with dbt_test__target as (

  select customer_id as unique_field
  from `starlit-gift-504722-c7`.`lumievre_marts`.`churn_features`
  where customer_id is not null

)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1


