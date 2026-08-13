# Génère un paiement pour chaque commande (facture) distincte.
# Défauts : paiement dupliqué (double capture), statut "réussi" avec montant à 0.
import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # remonte de pipelines/generation/ vers la racine

transactions = pd.read_parquet(PROJECT_ROOT / "data" / "processed" / "transactions_clean.parquet")

orders = transactions.groupby(["Invoice", "Customer ID"]).agg(
    invoice_date=("InvoiceDate", "min"),
    amount=("TotalPrice", "sum"),
).reset_index()

methods = ["credit_card", "paypal", "bank_transfer"]
payments = pd.DataFrame({
    "payment_id": [f"PAY-{i:06d}" for i in range(1, len(orders) + 1)],
    "invoice_id": orders["Invoice"].values,
    "customer_id": orders["Customer ID"].values,
    "payment_date": pd.to_datetime(orders["invoice_date"].values),
    "amount": orders["amount"].values,
    "method": np.random.choice(methods, size=len(orders), p=[0.55, 0.30, 0.15]),
    "status": "success",
})

# Défaut 1 : paiement dupliqué (~1.5%) -> la commande est payée deux fois dans le
# système de paiement (bug de double clic / retry réseau non idempotent)
dup_sample = payments.sample(frac=0.015, random_state=6).copy()
dup_sample["payment_id"] = dup_sample["payment_id"] + "-DUP"
payments = pd.concat([payments, dup_sample], ignore_index=True)

# Défaut 2 : statut "success" avec montant à 0 (~1%) -> erreur de synchronisation
# entre le gateway de paiement et le système de facturation
zero_idx = payments.sample(frac=0.01, random_state=7).index
payments.loc[zero_idx, "amount"] = 0.0

payments.to_parquet(PROJECT_ROOT / "data" / "generated" / "payments.parquet", index=False)

print("Paiements générés :", payments.shape)
print("Nb factures distinctes d'origine :", len(orders))
print("Paiements dupliqués :", payments["payment_id"].str.endswith("-DUP").sum())
print("Paiements 'success' à 0£ :", (payments["amount"] == 0).sum())