select
    cast(customer_id as int64) as customer_id,
    cast(preferred_channel as string) as preferred_channel,
    cast(consent_email as boolean) as consent_email,
    cast(consent_sms as boolean) as consent_sms,
    timestamp_micros(cast(opted_in_date / 1000 as int64)) as opted_in_date
from `starlit-gift-504722-c7`.`lumievre_raw`.`marketing_preferences`