# Lumièvre — Customer Analytics Platform

Un client fidèle sur trois finit par partir sans prévenir. Le pire : personne ne
le voit venir avant qu'il ne soit trop tard.

Ce projet répond à cette question avec des données réelles, pas des suppositions :
qui va partir, pourquoi, et comment agir avant. De la définition du problème
jusqu'à un modèle de détection déployé, en passant par une vraie plateforme cloud —
pas un notebook isolé.

## Sommaire

* [Contexte](#contexte)
* [Le besoin client](#le-besoin-client)
* [Analyse du besoin et recommandations](#analyse-du-besoin-et-recommandations)
* [Énoncé du problème spécifique (SMART)](#énoncé-du-problème-spécifique-smart)
* [Les données](#les-données)
* [Démonstration interactive](#démonstration-interactive)
* [Résultats](#résultats)
* [Architecture et plan du projet](#architecture-et-plan-du-projet)
* [Stack technique](#stack-technique)
* [Structure du repo](#structure-du-repo)
* [Installation](#installation)
* [Limites connues et prochaines étapes](#limites-connues-et-prochaines-étapes)

## Contexte

Lumièvre est une entreprise (fictive) de vente en ligne de cadeaux et de
décoration, active sur le marché britannique. Comme beaucoup d'e-commerces
installés depuis plusieurs années, ses données sont éclatées entre plusieurs
systèmes — ventes, service client, programme de fidélité, campagnes marketing —
qui n'ont jamais été reliés entre eux.

## Le besoin client

La direction marketing constate que des clients qui achetaient régulièrement
depuis des mois, parfois des années, cessent brutalement d'acheter — sans
réclamation, sans signal visible, sans qu'on sache pourquoi. La seule chose
qu'on constate, c'est l'absence.

La question posée est simple à formuler, difficile à résoudre :
*comment savoir qu'un client est en train de nous quitter, assez tôt pour
encore pouvoir agir ?*

## Analyse du besoin et recommandations

Avant de répondre, il a fallu comprendre ce qui était réellement demandé. Un
client qui part n'est pas un événement isolé : c'est la conséquence d'un
comportement qui change progressivement (moins d'achats, moins de contacts),
bien avant que le départ ne devienne visible.

Quatre leviers d'action ont été identifiés et priorisés avec la méthode
objectif / déclencheur / message / indicateur :

- Réactiver les clients qui montrent déjà des signes de désengagement marqués
- Prévenir les clients qui commencent tout juste à ralentir, avant que ce ne
  soit critique
- Encourager un deuxième achat rapide chez les nouveaux clients — le levier
  identifié comme le plus puissant du projet
- Fidéliser proactivement les meilleurs clients, avant qu'un signal négatif
  n'apparaisse

## Énoncé du problème spécifique (SMART)

Détecter, via un score comportemental construit sur l'historique d'achat et le
support client, les clients fidèles à risque de départ, pour permettre à
l'équipe marketing de les recontacter avant qu'ils ne partent pour de bon —
avec un modèle capable de repérer au moins 70 % des départs réels, pour faire
passer le taux de churn des clients fidèles de 29 % à 24 % sur un cycle de
6 mois.

## Les données

Le socle transactionnel s'appuie sur le dataset réel UCI Online Retail II
(plus d'un million de lignes de ventes, 2009-2011), complété par 7 sources
générées de façon réaliste pour reconstituer un environnement d'entreprise
complet : CRM, préférences marketing, programme de fidélité, support client,
retours, paiements, campagnes. Ces données incluent volontairement de vrais
défauts (valeurs manquantes, doublons, incohérences) pour refléter la réalité
d'un système d'information d'entreprise, pas un jeu de données déjà propre.

## Démonstration interactive

Une application interactive présente les résultats du projet en direct :
segmentation des clients, indicateurs clés, liste des clients à contacter en
priorité.

**Lien : [https://customer-behavior-analytics-platform.streamlit.app/]**

![Aperçu du dashboard](chemin/vers/ta/capture.png)


## Résultats

Le constat, mesuré sur les vraies données et non estimé :

- 29,0 % des clients fidèles finissent par partir
- 1,45 million de livres de chiffre d'affaires en jeu sur la période observée
- Le levier le plus puissant identifié : un client à un seul achat a 74 % de
  chances de partir, contre 59 % dès son deuxième achat

Le modèle de détection construit et validé objectivement (face à la méthode
simple déjà en place et face à une alternative plus complexe) repère 70 % des
départs réels, contre 50 % avec la méthode initiale — à un niveau de
précision quasiment identique. Avec un taux de réactivation de campagne
réaliste de 25 %, l'objectif est de préserver environ 220 000 £ de chiffre
d'affaires par cycle de 6 mois.


## Architecture et plan du projet

Le projet suit 13 phases, du cadrage métier jusqu'à l'industrialisation.

| Phase | Contenu | Statut |
|---|---|---|
| 1 | Cadrage métier (constat → SMART → cas d'usage → Lean Canvas) | Terminé |
| 2 | Architecture (GCP, décisions documentées, test de bout en bout) | Terminé |
| 3 | Modélisation (schéma de données, couches de transformation) | Terminé |
| 4 | Génération de 7 sources de données réalistes | Terminé |
| 5 | Exploration croisée (signaux validés : fréquence d'achat, support client) | Terminé |
| 6 | Entrepôt de données (GCS + BigQuery) | Terminé |
| 7 | Ingestion | Terminé |
| 8 | Transformation SQL (dbt) | Terminé |
| 9 | Dashboards (Looker Studio) | Terminé |
| 10 | Machine Learning (comparaison objective de 3 approches) | Terminé |
| 11 | Orchestration (Airflow via Docker) | Terminé |
| 12 | Monitoring & Qualité (tests automatisés, alerting) | Terminé |
| 13 | Industrialisation (CI/CD, sécurité, documentation) | Terminé |

Chaque décision structurante (périmètre, définitions métier, choix
techniques) est documentée dans un journal de 14 décisions d'architecture
(`docs/decisions/`).

## Stack technique
GCS (data lake) → BigQuery (warehouse) → dbt (transformation SQL) → Python
(ingestion, génération de données, ML) → Airflow/Docker (orchestration) →
MLflow (suivi des modèles) → Looker Studio et Streamlit (dashboards) → GitHub Actions (CI/CD).

## Structure du repo

docs/business/ -> cadrage métier complet (S.M.A.R.T., Lean Canvas)
docs/decisions/ -> 14 décisions d'architecture documentées
docs/architecture/ -> dictionnaire de données
notebooks/ -> exploration (jamais en production)
pipelines/generation/ -> génération des sources de données
pipelines/ingestion/ -> chargement GCS/BigQuery
lumievre_dbt/ -> transformation SQL (staging/intermediate/marts)
infrastructure/airflow/ -> orchestration (Docker + DAG)
ml/training/ -> entraînement et comparaison de modèles
dashboards/streamlit/ -> démonstration interactive
.github/workflows/ -> intégration continue

## Documentation clé
- [Cadrage métier](docs/business/01_cadrage.md)
- [Journal des décisions (14 ADR)](docs/decisions/)
- [Dictionnaire de données](docs/architecture/data_dictionary.md)

## Faire tourner le projet

1. Créer un projet GCP, activer BigQuery et Cloud Storage
2. `pip install -r requirements.txt`
3. Générer les données : `python pipelines/generation/generate_*.py`
4. Charger l'entrepôt : `python pipelines/ingestion/load_to_warehouse.py`
5. `cd lumievre_dbt && dbt run && dbt test`
6. Orchestration : `cd infrastructure/airflow && docker compose up -d`
7. Démonstration locale : `cd dashboards/streamlit && streamlit run app.py`

## Limites connues et prochaines étapes

Le cas d'usage du deuxième achat (le levier le plus puissant identifié) n'est
pas encore opérationnalisé — c'est la prochaine priorité. La diffusion réelle
des campagnes (email, SMS) n'est pas connectée : les résultats de campagne
utilisés pour valider le modèle sont simulés de façon réaliste, pas mesurés
en conditions réelles. L'authentification locale utilise des identifiants
personnels plutôt qu'un compte de service dédié — limite assumée pour un
projet portfolio, à corriger avant toute mise en production réelle. Un seul
environnement existe (pas de séparation dev/prod).