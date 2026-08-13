

  create or replace view `starlit-gift-504722-c7`.`lumievre_intermediate`.`int_transactions_cleaned`
  OPTIONS()
  as -- Reproduit le nettoyage validé en Phase 1 : hors annulations, hors codes
-- non-produits, UK uniquement (ADR-001), quantité/prix positifs, client identifié.
select
    invoice_id,
    stock_code,
    description,
    quantity,
    invoice_date,
    price,
    customer_id,
    country,
    quantity * price as total_price
from `starlit-gift-504722-c7`.`lumievre_staging`.`stg_online_retail__transactions`
where customer_id is not null
    and country = 'United Kingdom'
    and not starts_with(invoice_id, 'C')
    and upper(stock_code) not in ('POST', 'D', 'M', 'C2', 'BANK CHARGES', 'DOT', 'CRUK', 'AMAZONFEE', 'PADS', 'ADJUST', 'ADJUST2')
    and quantity > 0
    and price > 0;

