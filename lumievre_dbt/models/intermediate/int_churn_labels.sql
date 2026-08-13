-- Reproduit la méthode par coupure temporelle validée en Phase 1 (ADR-002) :
-- coupure au 10/06/2011, fenêtre d'observation avant, fenêtre de label de 6 mois après.
{% set cutoff = "'2011-06-10'" %}

with orders as (
    select distinct customer_id, invoice_id, invoice_date
    from {{ ref('int_transactions_cleaned') }}
),

observation as (
    select * from orders where invoice_date < timestamp({{ cutoff }})
),

label_window as (
    select * from orders where invoice_date >= timestamp({{ cutoff }})
),

eligible as (
    select
        customer_id,
        count(distinct invoice_id) as nb_orders_obs
    from observation
    group by customer_id
),

returned as (
    select distinct customer_id
    from label_window
    where customer_id in (select customer_id from eligible)
)

select
    e.customer_id,
    e.nb_orders_obs,
    e.nb_orders_obs >= 3 as is_loyal,
    r.customer_id is null as churned
from eligible e
left join returned r on e.customer_id = r.customer_id