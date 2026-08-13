-- Mart dédié aux cas d'usage marketing (C1/C2/C3/C4) — volontairement sans PII
-- (pas d'email, nom, prénom) : ce mart est fait pour être exposé à un dashboard.
select
    customer_id,
    country,
    signup_date,
    first_order_date,
    last_order_date,
    total_orders,
    total_revenue,
    is_loyal,
    churned,
    recency,
    frequency,
    monetary,
    coalesce(rfm_segment, 'non_fidele_ou_b2b') as rfm_segment,
    preferred_channel,
    consent_email,
    consent_sms,
    loyalty_tier,
    coalesce(nb_tickets, 0) as nb_tickets,
    low_satisfaction
from {{ ref('customer_360') }}
where is_loyal is not null  -- uniquement la population éligible aux cas d'usage