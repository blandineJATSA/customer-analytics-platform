-- Seule table que le pipeline ML est autorisé à lire (ADR-009).
-- Combine les signaux validés (RFM, satisfaction support) et les signaux non
-- validés individuellement mais gardés comme candidats (loyalty, marketing,
-- campagnes) - le modèle ML sert de filet de sécurité pour détecter des
-- interactions qu'une analyse bivariée simple ne peut pas voir (Phase 5).
-- has_returns et payments restent exclus : confondus avec la fréquence d'achat.


with campaign_obs as (
    select
        customer_id,
        count(*) as nb_sends,
        logical_or(opened) as ever_opened,
        logical_or(converted) as ever_converted
    from `starlit-gift-504722-c7`.`lumievre_staging`.`stg_marketing__campaign_sends`
    where sent_date < timestamp('2011-06-10')
    group by customer_id
)

select
    rfm.customer_id,
    rfm.recency,
    rfm.frequency,
    rfm.monetary,
    rfm.r_score,
    rfm.f_score,
    rfm.m_score,
    rfm.rfm_score,
    coalesce(c.nb_tickets, 0) as nb_tickets,
    coalesce(c.low_satisfaction, false) as low_satisfaction,
    coalesce(c.loyalty_tier, 'aucun') as loyalty_tier,
    coalesce(c.preferred_channel, 'inconnu') as preferred_channel,
    coalesce(c.consent_email, false) as consent_email,
    coalesce(camp.nb_sends, 0) as nb_sends,
    coalesce(camp.ever_opened, false) as ever_opened,
    coalesce(camp.ever_converted, false) as ever_converted,
    churn.churned
from `starlit-gift-504722-c7`.`lumievre_intermediate`.`int_customer_rfm` rfm
inner join `starlit-gift-504722-c7`.`lumievre_intermediate`.`int_churn_labels` churn on rfm.customer_id = churn.customer_id
left join `starlit-gift-504722-c7`.`lumievre_marts`.`customer_360` c on rfm.customer_id = c.customer_id
left join campaign_obs camp on rfm.customer_id = camp.customer_id