select
    cast(payment_id as string) as payment_id,
    cast(invoice_id as string) as invoice_id,
    cast(customer_id as int64) as customer_id,
    timestamp_micros(cast(payment_date / 1000 as int64)) as payment_date,
    cast(amount as numeric) as amount,
    cast(method as string) as method,
    cast(status as string) as status
from {{ source('raw', 'payments') }}