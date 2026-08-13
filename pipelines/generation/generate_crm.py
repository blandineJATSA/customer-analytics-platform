# Génère une table CRM synthétique pour les 5334 clients UK du périmètre V1.
# Défauts injectés volontairement (réalistes, pas aléatoires sans raison) :
# valeurs manquantes, erreurs de saisie, doublons.
import pandas as pd
import numpy as np
from faker import Faker
import random
import os

random.seed(42)
np.random.seed(42)
fake = Faker("en_GB")
Faker.seed(42)
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # remonte de pipelines/generation/ vers la racine

# On part des VRAIS customer_id du périmètre V1 (déjà nettoyés, UK uniquement)
transactions = pd.read_parquet(PROJECT_ROOT / "data" / "processed" / "transactions_clean.parquet")
customer_ids = transactions["Customer ID"].unique()

rows = []
for cid in customer_ids:
    rows.append({
        "customer_id": cid,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "country": "United Kingdom",
        "signup_date": pd.Timestamp("2008-01-01") + pd.Timedelta(days=random.randint(0, 1370)),
    })
crm = pd.DataFrame(rows)

# Défaut 1 : emails manquants (~4%) — un CRM réel a toujours des fiches incomplètes
missing_idx = crm.sample(frac=0.04, random_state=42).index
crm.loc[missing_idx, "email"] = None

# Défaut 2 : erreurs de saisie sur le pays (~2%) — saisie manuelle imparfaite
typo_idx = crm.sample(frac=0.02, random_state=1).index
crm.loc[typo_idx, "country"] = crm.loc[typo_idx, "country"].apply(
    lambda c: random.choice(["Untied Kingdom", "UK ", "united kingdom", "U.K."])
)

# Défaut 3 : doublons (même client, fiche créée deux fois avec un email différent, ~3%)
dup_sample = crm.sample(frac=0.03, random_state=2).copy()
dup_sample["email"] = dup_sample["email"].apply(
    lambda e: e.replace("@", ".dup@") if pd.notna(e) else fake.email()
)
crm = pd.concat([crm, dup_sample], ignore_index=True)



os.makedirs(PROJECT_ROOT / "data" / "generated", exist_ok=True)
crm["signup_date"] = pd.to_datetime(crm["signup_date"])
crm.to_parquet(PROJECT_ROOT / "data" / "generated" / "crm_customers.parquet", index=False)

print("CRM généré :", crm.shape)
print("Emails manquants :", crm["email"].isna().sum())
print("Doublons de customer_id :", crm["customer_id"].duplicated().sum())
print("Valeurs de pays distinctes :", crm["country"].unique())