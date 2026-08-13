# Dictionnaire de données (Résumé)

| Colonne | Description métier | Règles métier / Contraintes | Anomalies connues |
|---------|--------------------|-----------------------------|-------------------|
| **Invoice** | Identifiant de facture. Une facture peut contenir plusieurs lignes. Le préfixe `C` indique une annulation. | Doit être renseigné. Plusieurs lignes peuvent partager le même numéro de facture. | Factures d'annulation (`Cxxxxx`). |
| **StockCode** | Code unique identifiant un produit. | Un produit doit conserver le même code. | Présence de codes non commerciaux (`POST`, `BANK CHARGES`, `DOT`, `M`, etc.). |
| **Description** | Libellé du produit. | Un produit devrait avoir une description cohérente avec son `StockCode`. | Valeurs manquantes (~4 400) et libellés parfois non standard ou saisis manuellement. |
| **Quantity** | Nombre d'unités vendues. | Une vente normale a une quantité positive. | Valeurs négatives = retours, annulations ou ajustements de stock. Valeurs nulles à investiguer. |
| **InvoiceDate** | Date et heure de la transaction. | Doit correspondre à une date valide de vente. | Période couverte : **01/12/2009 → 09/12/2011**. Vérifier les dates incohérentes. |
| **Price** | Prix unitaire de l'article (£). | Le prix est généralement positif. | Prix à `0` pour certaines écritures non commerciales ou cadeaux. Valeurs négatives à investiguer. |
| **Customer ID** | Identifiant unique du client. | Un client doit conserver le même identifiant. | **22,77 %** de valeurs manquantes. Stocké en `float` mais devrait être converti en `Int64` ou `string`. |
| **Country** | Pays de livraison de la commande. | Doit appartenir à la liste des pays desservis. | **43 pays** présents, dont **91,9 %** des ventes au Royaume-Uni. Possibilité de restreindre l'analyse au UK. |

## Contrôles qualité à effectuer

- Vérifier les valeurs manquantes (`Description`, `Customer ID`).
- Identifier les factures d'annulation (`Invoice` commençant par `C`).
- Filtrer les codes non produits (`POST`, `BANK CHARGES`, `DOT`, etc.).
- Contrôler les quantités négatives ou nulles.
- Vérifier les prix nuls ou négatifs.
- Contrôler la cohérence `StockCode` ↔ `Description`.
- Vérifier la plage des dates de transaction.
- Standardiser les identifiants clients et les noms de pays.

## Décisions de cadrage additionnelles

- **Périmètre géographique** : analyse restreinte au Royaume-Uni (91,9% du volume). 
  Justification : comportement d'achat des autres pays potentiellement non comparable 
  (fréquence, saisonnalité, devise implicite) ; risque de biaiser la définition du churn 
  si mélangé. Décision prise en cadrage le [date], à documenter dans le rapport final client.
- **Table de référence retenue** : `df_clean` = ventes UK, clients identifiés, hors annulations/
  ajustements/frais, Quantity>0, Price>0. C'est la table qui servira de base à la table client (RFM).

  ## Doublons stricts

- 48 262 lignes dupliquées identifiées dans df_clean (mêmes valeurs sur toutes les colonnes).
- Vérification sur plusieurs factures échantillon : le nb de lignes uniques par facture 
  est proche du nb de lignes totales (jamais ~50%), ce qui exclut un bug d'export dupliquant 
  la facture entière.
- Hypothèse retenue : système de caisse n'agrégeant pas les ajouts répétés du même produit 
  au panier (plusieurs lignes à Quantity=1 au lieu d'une ligne à Quantity cumulée).
- Décision : conservées telles quelles. Chaque ligne = une unité réellement vendue ; 
  les supprimer sous-estimerait le CA et la fréquence d'achat réels du client.