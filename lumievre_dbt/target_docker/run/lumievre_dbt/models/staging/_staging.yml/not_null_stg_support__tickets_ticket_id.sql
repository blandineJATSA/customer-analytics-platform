select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select ticket_id
from `starlit-gift-504722-c7`.`lumievre_staging`.`stg_support__tickets`
where ticket_id is null



      
    ) dbt_internal_test