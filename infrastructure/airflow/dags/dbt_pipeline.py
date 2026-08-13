from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

DBT_DIR = "/opt/airflow/lumievre_dbt"


def alert_on_failure(context):
    task_id = context["task_instance"].task_id
    dag_id = context["dag"].dag_id
    execution_date = context["execution_date"]
    # Pour l'instant : log clair dans Airflow (visible dans l'onglet Logs).
    # Une vraie alerte (email/Slack) demanderait un serveur SMTP ou un webhook
    # externe, hors périmètre technique de ce portfolio (même logique que
    # l'ADR sur les campagnes marketing simulées, Phase 1).
    print(f"ALERTE : la tâche '{task_id}' du DAG '{dag_id}' a échoué le {execution_date}")
    print("Action recommandée : vérifier dbt test --select staging avant de relancer.")


default_args = {
    "on_failure_callback": alert_on_failure,
}

with DAG(
    dag_id="lumievre_dbt_pipeline",
    description="Exécute les modèles dbt : staging -> intermediate -> marts",
    schedule_interval="@monthly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["dbt", "lumievre"],
    default_args=default_args,
) as dag:

    run_staging = BashOperator(
        task_id="run_staging",
        bash_command=f"cd {DBT_DIR} && dbt run --select staging",
    )

    test_staging = BashOperator(
        task_id="test_staging",
        bash_command=f"cd {DBT_DIR} && dbt test --select staging",
    )

    run_intermediate = BashOperator(
        task_id="run_intermediate",
        bash_command=f"cd {DBT_DIR} && dbt run --select intermediate",
    )

    test_intermediate = BashOperator(
        task_id="test_intermediate",
        bash_command=f"cd {DBT_DIR} && dbt test --select intermediate",
    )

    run_marts = BashOperator(
        task_id="run_marts",
        bash_command=f"cd {DBT_DIR} && dbt run --select marts",
    )

    test_marts = BashOperator(
        task_id="test_marts",
        bash_command=f"cd {DBT_DIR} && dbt test --select marts",
    )

    run_staging >> test_staging >> run_intermediate >> test_intermediate >> run_marts >> test_marts