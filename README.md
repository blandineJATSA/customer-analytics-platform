# Lumièvre — Customer Analytics Platform

Plateforme de Customer Analytics end-to-end : détection du risque de churn client,
construite comme un vrai projet data d'entreprise — du cadrage métier chiffré
jusqu'à l'orchestration et le CI/CD.

## Contexte métier
Lumièvre est une entreprise fictive de vente de cadeaux/déco en ligne (périmètre UK).
Des clients fidèles cessent d'acheter sans explication. Ce projet détecte le risque
de churn suffisamment tôt pour permettre une action marketing ciblée.

**Résultat clé** : un modèle de régression logistique atteint 70% de recall à 52%
de précision, contre 50%/54% pour la règle RFM simple déjà en production — validé
par comparaison objective (Phase 10).

## Les 13 phases du projet

| Phase | Contenu | Statut |
|---|---|---|
| 1 | Cadrage métier (constat → SMART → cas d'usage → Lean Canvas) | ✅ |
| 2 | Architecture (GCP, ADR, smoke test) | ✅ |
| 3 | Modélisation (ERD, couches dbt, dictionnaire de données) | ✅ |
| 4 | Génération de 8 sources de données réalistes | ✅ |
| 5 | EDA croisée (signaux validés : fréquence, satisfaction support) | ✅ |
| 6 | Data Lake/Warehouse (GCS + BigQuery) | ✅ |
| 7 | Ingestion (scripts Python) | ✅ |
| 8 | Analytics Engineering (dbt : staging → intermediate → marts) | ✅ |
| 9 | Dashboards (Looker Studio) | ✅ |
| 10 | Machine Learning (régression logistique vs Random Forest vs baseline RFM) | ✅ |
| 11 | Orchestration (Airflow via Docker) | ✅ |
| 12 | Monitoring & Qualité (tests dbt, alerting) | ✅ |
| 13 | Industrialisation (CI/CD, sécurité, documentation) | ✅ |

## Stack technique
GCS (data lake) → BigQuery (warehouse) → dbt (transformation SQL) → Python
(ingestion, génération de données, ML) → Airflow/Docker (orchestration) →
MLflow (suivi des modèles) → Looker Studio (dashboards) → GitHub Actions (CI/CD).

## Structure du repo

docs/business/ -> cadrage métier complet (S.M.A.R.T., Lean Canvas)
docs/decisions/ -> 14 ADR documentant chaque décision technique/métier
docs/architecture/ -> dictionnaire de données
notebooks/ -> exploration (jamais en production, ADR-004)
pipelines/generation/ -> génération des 8 sources
pipelines/ingestion/ -> chargement GCS/BigQuery
lumievre_dbt/ -> transformation SQL (staging/intermediate/marts)
infrastructure/airflow/ -> orchestration (Docker + DAG)
ml/training/ -> entraînement et comparaison de modèles
.github/workflows/ -> CI (tests dbt sur chaque PR)

## Documentation clé
- [Cadrage métier](docs/business/01_cadrage.md)
- [Journal des décisions (14 ADR)](docs/decisions/)
- [Dictionnaire de données](docs/architecture/data_dictionary.md)

## Faire tourner le projet
1. Créer un projet GCP, activer BigQuery et Cloud Storage
2. `pip install -r requirements.txt`
3. Générer les données : `python pipelines/generation/generate_*.py`
4. Charger le warehouse : `python pipelines/ingestion/load_to_warehouse.py`
5. `cd lumievre_dbt && dbt run && dbt test`
6. Orchestration : `cd infrastructure/airflow && docker compose up -d`

## Limites connues et assumées
- Authentification locale via identifiants personnels (ADR-013) — un vrai
  déploiement production utiliserait un compte de service dédié partout,
  pas seulement en CI
- Diffusion réelle des campagnes marketing hors périmètre (données simulées)
- Un seul environnement (pas de séparation dev/prod)