select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select monetary
from `starlit-gift-504722-c7`.`lumievre_marts`.`churn_features`
where monetary is null



      
    ) dbt_internal_test