select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select churned
from `starlit-gift-504722-c7`.`lumievre_intermediate`.`int_churn_labels`
where churned is null



      
    ) dbt_internal_test