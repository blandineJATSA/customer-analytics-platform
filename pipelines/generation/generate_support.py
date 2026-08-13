# Génère les tickets de support — tous les clients n'en ont pas, certains en ont plusieurs.
# Défauts : dates invalides (résolution avant ouverture), score de satisfaction manquant.
from pathlib import Path

import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

PROJECT_ROOT = Path(__file__).resolve().parents[2]  # remonte de pipelines/generation/ vers la racine
crm = pd.read_parquet(PROJECT_ROOT / "data" / "generated" / "crm_customers.parquet")
real_customer_ids = crm["customer_id"].unique()

# ~25% des clients ont contacté le support au moins une fois
customers_with_tickets = np.random.choice(
    real_customer_ids, size=int(len(real_customer_ids) * 0.25), replace=False
)

churn_labels = pd.read_parquet(PROJECT_ROOT / "data" / "processed" / "churn_labels.parquet")
churned_customers = set(churn_labels.loc[churn_labels["Churned"], "Customer ID"])

categories = ["livraison", "produit_defectueux", "facturation", "retour", "autre"]
rows = []
ticket_counter = 1
for cid in customers_with_tickets:
    nb_tickets = np.random.choice([1, 2, 3], p=[0.7, 0.22, 0.08])
    for _ in range(nb_tickets):
        opened = pd.Timestamp("2010-01-01") + pd.Timedelta(days=random.randint(0, 700))
        resolution_days = random.randint(1, 14)
        resolved = opened + pd.Timedelta(days=resolution_days)

        # Score de satisfaction calculé À PART, avant de construire la ligne
        if random.random() < 0.35:
            score = None
        elif cid in churned_customers:
            score = random.choices([1, 2, 3, 4, 5], weights=[0.35, 0.30, 0.20, 0.10, 0.05])[0]
        else:
            score = random.choices([1, 2, 3, 4, 5], weights=[0.10, 0.15, 0.25, 0.25, 0.25])[0]

        rows.append({
            "ticket_id": f"TCK-{ticket_counter:06d}",
            "customer_id": cid,
            "category": random.choice(categories),
            "opened_date": opened,
            "resolved_date": resolved,
            "satisfaction_score": score,
        })
        ticket_counter += 1

support = pd.DataFrame(rows)

# Défaut : dates invalides — résolution enregistrée avant ouverture (~3%, bug de saisie
# où l'agent corrige la date d'ouverture après coup sans mettre à jour la résolution)
invalid_idx = support.sample(frac=0.03, random_state=3).index
support.loc[invalid_idx, "resolved_date"] = (
    support.loc[invalid_idx, "opened_date"] - pd.Timedelta(days=2)
)

support.to_parquet(PROJECT_ROOT / "data" / "generated" / "support_tickets.parquet", index=False)

print("Support généré :", support.shape)
print("Nb clients concernés :", support["customer_id"].nunique())
print("Scores de satisfaction manquants :", support["satisfaction_score"].isna().sum())
print("Tickets avec date de résolution avant ouverture :",
      (support["resolved_date"] < support["opened_date"]).sum())