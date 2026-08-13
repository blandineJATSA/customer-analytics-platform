

  create or replace view `starlit-gift-504722-c7`.`lumievre_intermediate`.`int_customer_rfm`
  OPTIONS()
  as -- Reproduit le RFM validé en Phase 1 : calculé uniquement sur la fenêtre
-- d'observation (pas de fuite de données), B2B exclus, scores par quartile.


with observation as (
    select *
    from `starlit-gift-504722-c7`.`lumievre_intermediate`.`int_transactions_cleaned`
    where invoice_date < timestamp('2011-06-10')
),

rfm_raw as (
    select
        customer_id,
        date_diff(date('2011-06-10'), date(max(invoice_date)), day) as recency,
        count(distinct invoice_id) as frequency,
        sum(total_price) as monetary,
        avg(quantity) as avg_qty_per_line
    from observation
    group by customer_id
),

loyal_only as (
    select r.*
    from rfm_raw r
    inner join `starlit-gift-504722-c7`.`lumievre_intermediate`.`int_churn_labels` c
        on r.customer_id = c.customer_id
    where c.is_loyal
),

-- Détection B2B : quantité moyenne/ligne au-dessus du p98 ET montant au-dessus du p95
thresholds as (
    select
        approx_quantiles(avg_qty_per_line, 100)[offset(98)] as qty_p98,
        approx_quantiles(monetary, 100)[offset(95)] as monetary_p95
    from loyal_only
),

retail_only as (
    select l.*
    from loyal_only l, thresholds t
    where not (l.avg_qty_per_line > t.qty_p98 and l.monetary > t.monetary_p95)
),

scored as (
    select
        *,
        ntile(4) over (order by recency desc) as r_score,
        ntile(4) over (order by frequency asc) as f_score,
        ntile(4) over (order by monetary asc) as m_score
    from retail_only
)

select
    customer_id,
    recency,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    (r_score + f_score + m_score) as rfm_score,
    case
        when (r_score + f_score + m_score) <= 5 then 'à_risque_critique'
        when (r_score + f_score + m_score) <= 8 then 'à_surveiller'
        else 'sain'
    end as rfm_segment
from scored;

