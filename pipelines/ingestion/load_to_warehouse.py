# Charge un fichier local vers GCS (zone raw) puis dans une table BigQuery brute.
# C'est la base du futur pipeline d'ingestion (Phase 7) ; on l'exécute manuellement
# pour l'instant, l'automatisation Airflow viendra en Phase 11.
from pathlib import Path
import shutil
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BUCKET = "lumievre-raw-starlit-gift-504722-c7"
PROJECT_ID = "starlit-gift-504722-c7"
DATASET = "lumievre_raw"


def ensure_tool(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        raise FileNotFoundError(
            f"La commande '{name}' est introuvable. Vérifiez que {name} est installé et présent dans le PATH."
        )
    return path


gcloud_cmd = ensure_tool("gcloud")
bq_cmd = ensure_tool("bq")

# (fichier local, chemin GCS, nom de table BigQuery)
FILES = [
    ("data/raw/online_retail_raw.parquet", "raw/online_retail/online_retail_raw.parquet", "online_retail_transactions"),
    ("data/generated/crm_customers.parquet", "raw/crm/crm_customers.parquet", "crm_customers"),
    ("data/generated/marketing_preferences.parquet", "raw/marketing/marketing_preferences.parquet", "marketing_preferences"),
    ("data/generated/loyalty_program.parquet", "raw/loyalty/loyalty_program.parquet", "loyalty_program"),
    ("data/generated/support_tickets.parquet", "raw/support/support_tickets.parquet", "support_tickets"),
    ("data/generated/returns.parquet", "raw/returns/returns.parquet", "returns"),
    ("data/generated/payments.parquet", "raw/payments/payments.parquet", "payments"),
    ("data/generated/campaigns.parquet", "raw/campaigns/campaigns.parquet", "campaigns"),
    ("data/generated/campaign_sends.parquet", "raw/campaigns/campaign_sends.parquet", "campaign_sends"),
]

for local_path, gcs_path, table_name in FILES:
    full_local = PROJECT_ROOT / local_path
    gcs_uri = f"gs://{BUCKET}/{gcs_path}"
    bq_table = f"{PROJECT_ID}:{DATASET}.{table_name}"

    print(f"\n=== {table_name} ===")
    subprocess.run([gcloud_cmd, "storage", "cp", str(full_local), gcs_uri], check=True)
    subprocess.run([
        bq_cmd, "load", "--source_format=PARQUET", "--replace", bq_table, gcs_uri
    ], check=True)
    print(f"OK -> {bq_table}")