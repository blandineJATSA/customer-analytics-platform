select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select customer_id
from `starlit-gift-504722-c7`.`lumievre_intermediate`.`int_customer_rfm`
where customer_id is null



      
    ) dbt_internal_test