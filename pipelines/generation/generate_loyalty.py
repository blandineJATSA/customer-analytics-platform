# Génère le programme de fidélité — tous les clients n'y sont pas inscrits.
# Défauts : clients orphelins (inscrits au programme mais jamais vus dans les
# commandes, ou l'inverse), historique incomplet (date d'inscription manquante).
import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # remonte de pipelines/generation/ vers la racine

crm = pd.read_parquet(PROJECT_ROOT / "data" / "generated" / "crm_customers.parquet")
real_customer_ids = crm["customer_id"].unique()

# ~55% des vrais clients sont inscrits au programme de fidélité
enrolled = np.random.choice(
    real_customer_ids, size=int(len(real_customer_ids) * 0.55), replace=False
)

tiers = ["Bronze", "Silver", "Gold"]
rows = []
for cid in enrolled:
    rows.append({
        "customer_id": cid,
        "loyalty_id": f"LOY-{cid}",
        "tier": random.choices(tiers, weights=[0.6, 0.3, 0.1])[0],
        "points_balance": random.randint(0, 5000),
        "enrollment_date": pd.to_datetime(
            None if random.random() < 0.06 else
            pd.Timestamp("2009-06-01") + pd.Timedelta(days=random.randint(0, 900))
        ),
    })

# Défaut : clients orphelins — des ID de fidélité qui ne correspondent à AUCUN vrai
# client (ex: migration d'un ancien système de fidélité jamais nettoyée)
orphan_ids = [90000 + i for i in range(25)]
for cid in orphan_ids:
    rows.append({
        "customer_id": cid,
        "loyalty_id": f"LOY-{cid}",
        "tier": random.choices(tiers, weights=[0.6, 0.3, 0.1])[0],
        "points_balance": random.randint(0, 5000),
        "enrollment_date": pd.Timestamp("2019-06-01") + pd.Timedelta(days=random.randint(0, 1800)),
    })

loyalty = pd.DataFrame(rows)
loyalty.to_parquet(PROJECT_ROOT / "data" / "generated" / "loyalty_program.parquet", index=False)

print("Loyalty généré :", loyalty.shape)
print("Nb inscrits parmi les vrais clients :", len(enrolled))
print("Nb clients orphelins (ID inexistant côté CRM/commandes) :",
      loyalty[~loyalty["customer_id"].isin(real_customer_ids)].shape[0])
print("Dates d'inscription manquantes :", loyalty["enrollment_date"].isna().sum())
print(loyalty["tier"].value_counts())