select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

with all_values as (

    select
        rfm_segment as value_field,
        count(*) as n_records

    from `starlit-gift-504722-c7`.`lumievre_intermediate`.`int_customer_rfm`
    group by rfm_segment

)

select *
from all_values
where value_field not in (
    'à_risque_critique','à_surveiller','sain_TYPO'
)



      
    ) dbt_internal_test