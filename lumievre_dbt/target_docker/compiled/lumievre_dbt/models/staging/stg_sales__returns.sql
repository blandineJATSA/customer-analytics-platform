select
    cast(return_id as string) as return_id,
    cast(customer_id as int64) as customer_id,
    cast(invoice_id as string) as invoice_id,
    cast(stock_code as string) as stock_code,
    timestamp_micros(cast(purchase_date / 1000 as int64)) as purchase_date,
    timestamp_micros(cast(return_date / 1000 as int64)) as return_date,
    cast(refund_amount as numeric) as refund_amount
from `starlit-gift-504722-c7`.`lumievre_raw`.`returns`