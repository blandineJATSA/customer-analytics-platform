# Journal de bord — Projet Lumièvre

## 2026-07-25 — Cadrage + réception des données

- Brief client reçu : base clients fidèles en érosion, sources non croisées (vente/CRM/service client).
- Objectif spécifique V1 posé : score de risque de départ + priorisation par valeur client.
- Décision : dataset UCI Online Retail II retenu (2009-2011), pas de vrai CRM fidélité/service client disponible → "fidèle" sera défini par le comportement d'achat.
- Fichier reçu : online_retail_II.xlsx, 2 feuilles (Year 2009-2010, Year 2010-2011), colonnes : Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country.
- Prochaine étape : audit qualité dans notebooks/01_exploration_qualite.ipynb.

## 2026-07-26 - 

## Périmètre retenu pour l'analyse clients

Sur 1 067 371 lignes brutes, on distingue :

| Filtre | Règle | Lignes concernées | Décision |
|---|---|---|---|
| Annulations | Invoice commence par "C" | 19 494 (1,83%) | Exclues des ventes ; conservées à part comme signal "retour/annulation" (feature possible plus tard) |
| Écritures non-produits | StockCode ∈ {POST, DOT, D, M, C2, BANK CHARGES, ADJUST, ADJUST2, AMAZONFEE, CRUK} | 5 703 | Exclues : frais, remises, ajustements comptables, pas des ventes |
| Quantity négative hors annulation | Quantity < 0 et Invoice pas "C" | 3 457 | Exclues : casse, pertes, corrections de stock (confirmé via Description : "damages", "lost", "sold as gold"...) |
| Price <= 0 | Price ≤ 0 | 6 207 | Exclues (recoupe en partie les catégories au-dessus) |
| Customer ID manquant | Customer ID = NaN | 243 007 (22,77%) | Exclues de l'analyse par client ; CA associé isolé et chiffré séparément pour la cliente |

## Colonnes

| Colonne | Type | Description métier | Anomalies connues |
|---|---|---|---|
| Invoice | str | Identifiant facture ; préfixe "C" = annulation | — |
| StockCode | str | Code produit | Contient des codes non-produits (voir filtre ci-dessus) |
| Description | str | Libellé produit | ~4 400 valeurs manquantes ; libellés parfois manuels/non standard |
| Quantity | int | Quantité vendue | Négatif = annulation ou ajustement stock |
| InvoiceDate | datetime | Date/heure de la transaction | Plage 2009-12-01 → 2011-12-09 |
| Price | float | Prix unitaire (£) | Peut être 0 pour écritures non-commerciales |
| Customer ID | float (⚠️) | Identifiant client | 22,77% manquants ; type float à corriger en Int64/str |
| Country | str | Pays de livraison | 43 valeurs, 91,9% UK — périmètre à restreindre ? |

## [date] — Nettoyage des données validé

- Règle de nettoyage cumulée définie et appliquée (annulations, codes non-produits, 
  quantités/prix invalides, Customer ID manquant, périmètre UK).
- Décision de restreindre à UK validée avec l'utilisateur avant codage.
- Prochaine étape : construction de la table client (RFM) pour poser le constat chiffré.

## [date] — Doublons stricts analysés et conservés
- 48 262 doublons stricts examinés sur échantillon de factures.
- Confirmé : comportement de caisse (produits ajoutés séparément), pas un bug technique.
- Décision : aucune déduplication appliquée sur df_clean.

## [date] — Analyse de la distribution des écarts inter-achats

- 24 686 écarts calculés sur les clients UK identifiés.
- Distribution non bimodale : décroissance continue (pic à 6-11j, longue traîne jusqu'à 714j).
- Pas de "coude" net isolé → seuil de churn ne peut pas être déduit de la seule forme statistique,
  doit être choisi en croisant percentile + logique métier.
- Deux seuils candidats retenus pour test :
  - P75 = 71 jours (~2,5 mois) : détection précoce, plus de faux positifs
  - P90 = 149 jours (~5 mois) : détection plus tardive, plus fiable statistiquement
- Prochaine étape : comparer le nb de clients "à risque" avec chaque seuil pour choisir
  celui qui reste actionnable pour le marketing.
  