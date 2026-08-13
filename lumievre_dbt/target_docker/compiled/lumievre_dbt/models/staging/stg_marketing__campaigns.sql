select
    cast(campaign_id as string) as campaign_id,
    cast(campaign_type as string) as campaign_type,
    timestamp_micros(cast(sent_date / 1000 as int64)) as sent_date
from `starlit-gift-504722-c7`.`lumievre_raw`.`campaigns`