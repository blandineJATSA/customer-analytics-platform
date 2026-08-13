

  create or replace view `starlit-gift-504722-c7`.`lumievre_staging`.`stg_support__tickets`
  OPTIONS()
  as select
    cast(ticket_id as string) as ticket_id,
    cast(customer_id as int64) as customer_id,
    cast(category as string) as category,
    timestamp_micros(cast(opened_date / 1000 as int64)) as opened_date,
    timestamp_micros(cast(resolved_date / 1000 as int64)) as resolved_date,
    cast(satisfaction_score as int64) as satisfaction_score
from `starlit-gift-504722-c7`.`lumievre_raw`.`support_tickets`;

