# Export brut, SANS AUCUN FILTRE (pas de filtre UK, pas d'exclusion de codes,
# pas de retrait des annulations) -> ces règles doivent vivre en SQL dbt (ADR-007),
# pas être décidées ici en Python.
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
xl = pd.ExcelFile(PROJECT_ROOT / "data" / "raw" / "online_retail_II.xlsx")
df = pd.concat([xl.parse("Year 2009-2010"), xl.parse("Year 2010-2011")], ignore_index=True)

df = df.rename(columns={
    "Invoice": "invoice_id", "StockCode": "stock_code", "Description": "description",
    "Quantity": "quantity", "InvoiceDate": "invoice_date", "Price": "price",
    "Customer ID": "customer_id", "Country": "country",
})

df = df.astype({
    "invoice_id": "string",
    "stock_code": "string",
    "customer_id": "string",
    "description" : "string",
})
out_path = PROJECT_ROOT / "data" / "raw" / "online_retail_raw.parquet"
df.to_parquet(out_path, index=False)
print("Export brut :", df.shape, "->", out_path)