# Génère un historique d'événements client (journal d'activité), à partir de
# toutes les sources déjà générées. Défauts : doublons d'événements, dates invalides.
import pandas as pd
import numpy as np
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # remonte de pipelines/generation/ vers la racine

crm = pd.read_parquet(PROJECT_ROOT / "data" / "generated" / "crm_customers.parquet")
transactions = pd.read_parquet(PROJECT_ROOT / "data" / "processed" / "transactions_clean.parquet")
support = pd.read_parquet(PROJECT_ROOT / "data" / "generated" / "support_tickets.parquet")
loyalty = pd.read_parquet(PROJECT_ROOT / "data" / "generated" / "loyalty_program.parquet")

events = []

# Événement : inscription CRM
for _, row in crm.dropna(subset=["signup_date"]).iterrows():
    events.append({
        "customer_id": row["customer_id"],
        "event_type": "signup",
        "event_date": row["signup_date"],
    })

# Événement : premier achat par facture (pas chaque ligne produit)
first_orders = transactions.groupby("Customer ID")["InvoiceDate"].min().reset_index()
for _, row in first_orders.iterrows():
    events.append({
        "customer_id": row["Customer ID"],
        "event_type": "first_purchase",
        "event_date": row["InvoiceDate"],
    })

# Événement : ouverture de ticket support
for _, row in support.iterrows():
    events.append({
        "customer_id": row["customer_id"],
        "event_type": "support_ticket_opened",
        "event_date": row["opened_date"],
    })

# Événement : inscription au programme fidélité
for _, row in loyalty.dropna(subset=["enrollment_date"]).iterrows():
    events.append({
        "customer_id": row["customer_id"],
        "event_type": "loyalty_enrollment",
        "event_date": row["enrollment_date"],
    })

history = pd.DataFrame(events)
history["event_date"] = pd.to_datetime(history["event_date"])

# Défaut 1 : doublons d'événements (~2%) -> événement loggé deux fois par le
# système de tracking (répétition classique de journalisation applicative)
dup_sample = history.sample(frac=0.02, random_state=9)
history = pd.concat([history, dup_sample], ignore_index=True)

# Défaut 2 : dates invalides dans le futur (~1%) -> erreur de fuseau horaire/timestamp
invalid_idx = history.sample(frac=0.01, random_state=10).index
history.loc[invalid_idx, "event_date"] = pd.Timestamp("2099-01-01")

history.to_parquet(PROJECT_ROOT / "data" / "generated" / "customer_history.parquet", index=False)

print("Historique généré :", history.shape)
print(history["event_type"].value_counts())
print("Doublons exacts :", history.duplicated().sum())
print("Dates dans le futur (>2012) :", (history["event_date"].dt.year > 2012).sum())