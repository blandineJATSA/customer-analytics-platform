select
    cast(customer_id as int64) as customer_id,
    cast(first_name as string) as first_name,
    cast(last_name as string) as last_name,
    cast(email as string) as email,
    cast(phone as string) as phone,
    cast(country as string) as country,
    date(timestamp_micros(cast(signup_date / 1000 as int64))) as signup_date
from `starlit-gift-504722-c7`.`lumievre_raw`.`crm_customers`