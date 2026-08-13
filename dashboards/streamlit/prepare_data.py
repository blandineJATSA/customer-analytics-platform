# Extrait les données de BigQuery vers 3 petits fichiers locaux (CSV/JSON)
# pour que la démo Streamlit démarre instantanément, sans interroger
# BigQuery à chaque rechargement de page.
import json
from pathlib import Path

import pandas as pd
import pandas_gbq

PROJECT_ID = "starlit-gift-504722-c7"
OUT_DIR = Path(__file__).resolve().parent

# 1. Les clients fidèles retail, avec leur segment RFM
rfm = pandas_gbq.read_gbq(f"""
    SELECT customer_id, recency, frequency, monetary, rfm_segment AS segment, churned
    FROM `{PROJECT_ID}.lumievre_marts.customer_risk_segments`
    WHERE rfm_segment != 'non_fidele_ou_b2b'
""", project_id=PROJECT_ID)
rfm.to_csv(OUT_DIR / "rfm_demo.csv", index=False)
print("rfm_demo.csv :", rfm.shape)

# 2. Le taux de churn par nombre de commandes (l'insight le plus fort du projet)
freq = pandas_gbq.read_gbq(f"""
    SELECT nb_orders_obs, COUNT(*) AS n,
           AVG(CASE WHEN churned THEN 1.0 ELSE 0.0 END) AS churn_rate
    FROM `{PROJECT_ID}.lumievre_intermediate.int_churn_labels`
    GROUP BY nb_orders_obs
    HAVING COUNT(*) >= 20
    ORDER BY nb_orders_obs
""", project_id=PROJECT_ID)
freq.to_csv(OUT_DIR / "churn_by_frequency.csv", index=False)
print("churn_by_frequency.csv :", freq.shape)

# 3. Les indicateurs agrégés
loyal = pandas_gbq.read_gbq(f"""
    SELECT COUNT(*) AS nb_loyal,
           AVG(CASE WHEN churned THEN 1.0 ELSE 0.0 END) AS churn_rate
    FROM `{PROJECT_ID}.lumievre_intermediate.int_churn_labels`
    WHERE is_loyal
""", project_id=PROJECT_ID)

kpis = {
    "loyal": int(loyal["nb_loyal"][0]),
    "loyal_churn_rate": float(loyal["churn_rate"][0]),
    "total_revenue_loyal": float(rfm["monetary"].sum()),
    "revenue_at_risk": float(rfm.loc[rfm["churned"], "monetary"].sum()),
}
with open(OUT_DIR / "kpis.json", "w") as f:
    json.dump(kpis, f, indent=2)
print("kpis.json :", kpis)