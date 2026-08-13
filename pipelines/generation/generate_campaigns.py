# Génère les campagnes et leurs envois — la donnée manquante identifiée dans
# notre étude de faisabilité (Phase 1) pour mesurer C1/C2/C3.
# Défauts : tracking manquant sur les anciens envois, envoi à un client orphelin.
import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # remonte de pipelines/generation/ vers la racine

crm = pd.read_parquet(PROJECT_ROOT / "data" / "generated" / "crm_customers.parquet")
real_customer_ids = crm["customer_id"].unique()

# 12 campagnes sur la période, de types variés
campaign_types = ["reactivation", "newsletter", "promo_saisonniere", "bienvenue"]
campaigns = pd.DataFrame({
    "campaign_id": [f"CMP-{i:03d}" for i in range(1, 13)],
    "campaign_type": [random.choice(campaign_types) for _ in range(12)],
    "sent_date": [pd.Timestamp("2010-06-01") + pd.Timedelta(days=60 * i) for i in range(12)],
})

rows = []
send_counter = 1
for _, camp in campaigns.iterrows():
    # chaque campagne cible ~40% des clients au hasard
    targeted = np.random.choice(real_customer_ids, size=int(len(real_customer_ids) * 0.4), replace=False)
    for cid in targeted:
        opened = random.random() < 0.35       # 35% taux d'ouverture
        clicked = opened and random.random() < 0.30   # 30% des ouvertures cliquent
        converted = clicked and random.random() < 0.25 # 25% des clics convertissent (réachat)
        rows.append({
            "send_id": f"SND-{send_counter:07d}",
            "campaign_id": camp["campaign_id"],
            "customer_id": cid,
            "sent_date": camp["sent_date"],
            "opened": opened,
            "clicked": clicked,
            "converted": converted,
        })
        send_counter += 1

sends = pd.DataFrame(rows)

# Défaut 1 : tracking manquant sur les envois les plus anciens (avant 2011)
# -> l'outil de tracking a été mis en place en cours de route, comme dans une vraie entreprise
old_mask = sends["sent_date"] < pd.Timestamp("2011-01-01")
sends["opened"] = sends["opened"].astype("boolean")
sends["clicked"] = sends["clicked"].astype("boolean")
sends["converted"] = sends["converted"].astype("boolean")
sends.loc[old_mask, ["opened", "clicked", "converted"]] = None

# Défaut 2 : envoi à des clients orphelins (~1%) -> liste d'envoi importée d'un
# ancien outil marketing non synchronisé avec le CRM actuel
orphan_sends = sends.sample(frac=0.01, random_state=8).copy()
orphan_sends["customer_id"] = [90000 + i for i in range(len(orphan_sends))]
sends = pd.concat([sends, orphan_sends], ignore_index=True)

campaigns.to_parquet(PROJECT_ROOT / "data" / "generated" / "campaigns.parquet", index=False)
sends.to_parquet(PROJECT_ROOT / "data" / "generated" / "campaign_sends.parquet", index=False)

print("Campagnes générées :", campaigns.shape)
print("Envois générés :", sends.shape)
print("Taux d'ouverture réel :", sends["opened"].mean())
print("Envois avec tracking manquant (NaT) :", sends["opened"].isna().sum())
print("Envois à des clients orphelins :", (~sends["customer_id"].isin(real_customer_ids)).sum())