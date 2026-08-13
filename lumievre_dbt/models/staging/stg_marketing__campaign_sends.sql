select
    cast(send_id as string) as send_id,
    cast(campaign_id as string) as campaign_id,
    cast(customer_id as int64) as customer_id,
    timestamp_micros(cast(sent_date / 1000 as int64)) as sent_date,
    cast(opened as boolean) as opened,
    cast(clicked as boolean) as clicked,
    cast(converted as boolean) as converted
from {{ source('raw', 'campaign_sends') }}