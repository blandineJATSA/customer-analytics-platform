# Génère les préférences marketing pour chaque client CRM.
# Défauts : consentement manquant, incohérence canal préféré vs consentement.
import pandas as pd
import numpy as np
from faker import Faker
import random

random.seed(42)
np.random.seed(42)
Faker.seed(42)
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # remonte de pipelines/generation/ vers la racine

crm = pd.read_parquet(PROJECT_ROOT / "data" / "generated" / "crm_customers.parquet")
customer_ids = crm["customer_id"].unique()  # dédupliqué : une préférence par vrai client

channels = ["email", "sms", "postal", "none"]
rows = []
for cid in customer_ids:
    consent_email = random.random() < 0.75  # 75% ont donné leur consentement email
    rows.append({
        "customer_id": cid,
        "preferred_channel": random.choices(channels, weights=[0.6, 0.15, 0.1, 0.15])[0],
        "consent_email": consent_email,
        "consent_sms": random.random() < 0.35,
        "opted_in_date": pd.to_datetime(
            None if random.random() < 0.05 else
            pd.Timestamp("2009-01-01") + pd.Timedelta(days=random.randint(0, 1000))
        ),
    })
marketing = pd.DataFrame(rows)

# Défaut : incohérence — canal préféré "email" mais consentement email refusé (~ce qui arrive
# quand une préférence déclarée n'a pas été synchronisée avec le vrai statut RGPD)
incoherent_idx = marketing[
    (marketing["preferred_channel"] == "email") & (~marketing["consent_email"])
].index
print(f"Incohérences canal/consentement déjà présentes naturellement : {len(incoherent_idx)}")

marketing.to_parquet(PROJECT_ROOT / "data" / "generated" / "marketing_preferences.parquet", index=False)
print("Marketing généré :", marketing.shape)
print("Consentement email manquant (NaT date d'inscription) :", marketing["opted_in_date"].isna().sum())
print(marketing["preferred_channel"].value_counts())