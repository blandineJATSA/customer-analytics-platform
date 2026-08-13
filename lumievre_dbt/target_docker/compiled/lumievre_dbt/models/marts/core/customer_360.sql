-- Table centrale (ADR-009) : une ligne = un client, assemblant CRM, commandes,
-- fidélité, support, marketing, churn et RFM.
with crm_ranked as (
    select *, row_number() over (partition by customer_id order by signup_date asc) as rn
    from `starlit-gift-504722-c7`.`lumievre_staging`.`stg_crm__customers`
),
crm_dedup as (
    select * except(rn) from crm_ranked where rn = 1
),

order_agg as (
    select
        customer_id,
        min(invoice_date) as first_order_date,
        max(invoice_date) as last_order_date,
        count(distinct invoice_id) as total_orders,
        sum(total_price) as total_revenue
    from `starlit-gift-504722-c7`.`lumievre_intermediate`.`int_transactions_cleaned`
    group by customer_id
),

support_agg as (
    select
        customer_id,
        count(*) as nb_tickets,
        avg(satisfaction_score) as avg_satisfaction
    from `starlit-gift-504722-c7`.`lumievre_staging`.`stg_support__tickets`
    group by customer_id
)

select
    crm_dedup.customer_id,
    crm_dedup.first_name,
    crm_dedup.last_name,
    crm_dedup.email,
    crm_dedup.country,
    crm_dedup.signup_date,
    order_agg.first_order_date,
    order_agg.last_order_date,
    order_agg.total_orders,
    order_agg.total_revenue,
    mkt.preferred_channel,
    mkt.consent_email,
    mkt.consent_sms,
    loy.tier as loyalty_tier,
    loy.points_balance,
    sup.nb_tickets,
    sup.avg_satisfaction,
    sup.avg_satisfaction < 3 as low_satisfaction,
    churn.is_loyal,
    churn.churned,
    rfm.recency,
    rfm.frequency,
    rfm.monetary,
    rfm.rfm_score,
    rfm.rfm_segment
from crm_dedup
left join order_agg on crm_dedup.customer_id = order_agg.customer_id
left join `starlit-gift-504722-c7`.`lumievre_staging`.`stg_marketing__preferences` mkt on crm_dedup.customer_id = mkt.customer_id
left join `starlit-gift-504722-c7`.`lumievre_staging`.`stg_loyalty__program` loy on crm_dedup.customer_id = loy.customer_id
left join support_agg sup on crm_dedup.customer_id = sup.customer_id
left join `starlit-gift-504722-c7`.`lumievre_intermediate`.`int_churn_labels` churn on crm_dedup.customer_id = churn.customer_id
left join `starlit-gift-504722-c7`.`lumievre_intermediate`.`int_customer_rfm` rfm on crm_dedup.customer_id = rfm.customer_id