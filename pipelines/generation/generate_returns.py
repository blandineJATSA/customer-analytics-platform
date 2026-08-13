# Génère les retours produits, à partir des vraies transactions.
# Défauts : montant remboursé incohérent (> montant acheté), date de retour
# antérieure à la date d'achat (bug d'horodatage).
import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # remonte de pipelines/generation/ vers la racine

transactions = pd.read_parquet(PROJECT_ROOT / "data" / "processed" / "transactions_clean.parquet")

# ~6% des lignes de commande donnent lieu à un retour (taux réaliste e-commerce)
returned_lines = transactions.sample(frac=0.06, random_state=42).copy()

returns = pd.DataFrame({
    "return_id": [f"RET-{i:06d}" for i in range(1, len(returned_lines) + 1)],
    "customer_id": returned_lines["Customer ID"].values,
    "invoice_id": returned_lines["Invoice"].values,
    "stock_code": returned_lines["StockCode"].values,
    "purchase_date": pd.to_datetime(returned_lines["InvoiceDate"].values),
    "return_date": pd.to_datetime(returned_lines["InvoiceDate"].values) + pd.to_timedelta(
        np.random.randint(1, 21, size=len(returned_lines)), unit="D"
    ),
    "refund_amount": (returned_lines["Quantity"] * returned_lines["Price"]).values,
})

# Défaut 1 : montant remboursé incohérent (remboursement > montant acheté, ~2%)
# -> erreur de saisie manuelle d'un montant de remboursement
overpay_idx = returns.sample(frac=0.02, random_state=4).index
returns.loc[overpay_idx, "refund_amount"] *= np.random.uniform(1.5, 3.0, size=len(overpay_idx))

# Défaut 2 : date de retour AVANT la date d'achat (~2%) -> bug d'horodatage système
invalid_date_idx = returns.sample(frac=0.02, random_state=5).index
returns.loc[invalid_date_idx, "return_date"] = (
    returns.loc[invalid_date_idx, "purchase_date"] - pd.Timedelta(days=3)
)

returns.to_parquet(PROJECT_ROOT / "data" / "generated" / "returns.parquet", index=False)

print("Retours générés :", returns.shape)
print("Retours avec date invalide (avant l'achat) :",
      (returns["return_date"] < returns["purchase_date"]).sum())
print("Retours avec remboursement > montant ligne d'origine :",
      (returns["refund_amount"] > (returned_lines["Quantity"].values * returned_lines["Price"].values)).sum())