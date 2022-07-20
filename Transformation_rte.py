# Librairies
import pandas as pd
import os


# Path
path = os.path.dirname(__file__)


# Lecture du fichier RTE
df_rte = pd.read_csv((path + '\\Data\\RTE_eco2mix_regional_cons_def.csv'), sep = ';')


# Traitement des données date
## Création des champs Mois et Annee
df_rte['Mois'] = pd.to_datetime(df_rte['Date']).dt.strftime('%Y-%m')
df_rte['Annee'] = pd.to_datetime(df_rte['Date'], format='%Y-%m-%d').dt.year
df_rte['Annee'] = df_rte['Annee'].astype('int')

## Ajout du jour de la semaine et du numéro de semaine
df_rte['Jour_semaine'] = pd.to_datetime(df_rte['Date']).dt.dayofweek
df_rte['Semaine'] = pd.to_datetime(df_rte['Date']).dt.strftime('%Y-%V')


# Conservation des colonnes identifiées comme utiles
# Column 26 notamment est supprimée car elle ne comprend que des NA
colonnes_a_conserver = [
    'Code INSEE région', 'Région', 'Nature', 'Annee', 'Mois', 'Semaine', 
    'Date', 'Jour_semaine', 'Heure', 'Date - Heure', 'Consommation (MW)',
    'Thermique (MW)', 'Nucléaire (MW)', 'Eolien (MW)', 'Solaire (MW)',
    'Hydraulique (MW)', 'Pompage (MW)', 'Bioénergies (MW)', 
    'Ech. physiques (MW)'
]

df_rte = df_rte[colonnes_a_conserver]


# Suppression des colonnes qui ne comportent que des valeurs manquantes 
# (cas des 12 premières valeurs)
df_rte = df_rte.dropna(axis = 0, how = 'all', subset = ['Consommation (MW)',
    'Thermique (MW)', 'Nucléaire (MW)', 'Eolien (MW)', 'Solaire (MW)',
    'Hydraulique (MW)', 'Pompage (MW)', 'Bioénergies (MW)',
    'Ech. physiques (MW)'
]
)


# Remplacement des valeurs manquantes
''' Les valeurs manquantes correspondent à des données incohérentes (par
exemple s'il n'y pas de production nucléaire dans une région, la valeur
sera manquante).
On remplace donc les valeurs manquantes par 0.'''

df_rte = df_rte.fillna(0)


# Passage des données au format integer
df_rte[
    ['Consommation (MW)', 'Thermique (MW)', 'Nucléaire (MW)',
    'Eolien (MW)', 'Solaire (MW)', 'Hydraulique (MW)', 'Pompage (MW)',
    'Bioénergies (MW)', 'Ech. physiques (MW)']
    ] = df_rte[
        ['Consommation (MW)',
        'Thermique (MW)',
        'Nucléaire (MW)',
        'Eolien (MW)',
        'Solaire (MW)',
        'Hydraulique (MW)',
        'Pompage (MW)',
        'Bioénergies (MW)',
        'Ech. physiques (MW)'
        ]].astype(int)


# Création d'une colonne de production totale
df_rte['Production totale (MW)'] = (
    df_rte['Thermique (MW)'] + 
    df_rte['Nucléaire (MW)'] + 
    df_rte['Eolien (MW)'] + 
    df_rte['Solaire (MW)'] + 
    df_rte['Hydraulique (MW)'] + 
    df_rte['Pompage (MW)'] + 
    df_rte['Bioénergies (MW)']
    )


# Création des fonctions d'agrégation
'''
- Les données de consommation et de production sont agrégées en sommant les données.
- Les données TCO/TCH sont agrégées par leur moyenne.
'''

agregation = dict.fromkeys(
    ('Consommation (MW)', 'Thermique (MW)', 'Nucléaire (MW)',
     'Eolien (MW)', 'Solaire (MW)', 'Hydraulique (MW)', 'Pompage (MW)',
     'Bioénergies (MW)', 'Ech. physiques (MW)', 'Production totale (MW)'
     ),
     'sum'
)


# Création d'un df agrégé par jour et par région
df_rte_jour_regions = df_rte.groupby(
    ['Date', 'Jour_semaine', 'Annee', 'Mois', 'Code INSEE région', 'Région'],
    as_index=False).agg(
    agregation
)


# Création d'un df agrégé par mois et par région
df_rte_mois_regions = df_rte.groupby(
    ['Annee', 'Mois', 'Code INSEE région', 'Région'],
    as_index=False).agg(
    agregation
)


# # Création d'un df agrégé par jour (somme de toutes les régions)
# df_rte_jour = df_rte_jour_regions.groupby(
#     ['Date', 'Jour_semaine', 'Annee', 'Mois'],
#     as_index=False).agg(
#     agregation
# )


# Enregistrement des df
df_rte.to_csv(
    path + '\\Data\\rte.csv',
    sep=';',
    index=False,
    encoding='utf-8'
)

df_rte_jour_regions.to_csv(
    path + '\\Data\\rte_jour_regions.csv',
    sep=';',
    index=False,
    encoding='utf-8'
)

df_rte_mois_regions.to_csv(
    path + '\\Data\\rte_mois_regions.csv',
    sep=';',
    index=False,
    encoding='utf-8'
)

# df_rte_jour.to_csv(
#     path + '\\Data\\rte_jour.csv',
#     sep=';',
#     index=False,
#     encoding='utf-8'
# )