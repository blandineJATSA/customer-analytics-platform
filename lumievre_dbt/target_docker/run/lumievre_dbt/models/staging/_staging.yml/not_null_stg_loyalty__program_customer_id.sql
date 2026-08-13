select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select customer_id
from `starlit-gift-504722-c7`.`lumievre_staging`.`stg_loyalty__program`
where customer_id is null



      
    ) dbt_internal_test