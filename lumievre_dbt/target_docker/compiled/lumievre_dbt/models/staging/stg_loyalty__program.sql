select
    cast(customer_id as int64) as customer_id,
    cast(loyalty_id as string) as loyalty_id,
    cast(tier as string) as tier,
    cast(points_balance as int64) as points_balance,
    timestamp_micros(cast(enrollment_date / 1000 as int64)) as enrollment_date
from `starlit-gift-504722-c7`.`lumievre_raw`.`loyalty_program`