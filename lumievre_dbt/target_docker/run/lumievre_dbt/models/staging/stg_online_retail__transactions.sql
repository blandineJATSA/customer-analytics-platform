

  create or replace view `starlit-gift-504722-c7`.`lumievre_staging`.`stg_online_retail__transactions`
  OPTIONS()
  as -- Copie typée du brut, aucune règle métier (ADR-007)
select
    cast(invoice_id as string) as invoice_id,
    cast(stock_code as string) as stock_code,
    cast(description as string) as description,
    cast(quantity as int64) as quantity,
    cast(invoice_date as timestamp) as invoice_date,
    cast(price as numeric) as price,
    cast(cast(customer_id as float64) as int64) as customer_id,
    cast(country as string) as country
from `starlit-gift-504722-c7`.`lumievre_raw`.`online_retail_transactions`;

