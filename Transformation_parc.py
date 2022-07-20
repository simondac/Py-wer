# Librairires
import pandas as pd
import os


# Path
path = os.path.dirname(__file__)


# Lecture du fichier capa installées
df_parc = pd.read_csv((path + '\\Data\\parc-prod-par-filiere.csv'), sep = ';')



# Suppression des colonnes fioul, charbon et gaz dont la somme est la colonne thermique fossile
df_parc = df_parc.drop(
    ['Parc fioul (MW)', 'Parc charbon (MW)', 'Parc gaz (MW)'], 
    axis=1
    )


# On renomme les colonnes pour correspondre aux noms de colonnes du fichier de production
df_parc = df_parc.rename(
    {
        'Parc thermique fossile (MW)':'Thermique (MW)', 
        'Parc hydraulique (MW)':'Hydraulique (MW)', 
        'Parc nucleaire (MW)':'Nucléaire (MW)', 
        'Parc solaire (MW)':'Solaire (MW)', 
        'Parc eolien (MW)':'Eolien (MW)', 
        'Parc bioenergie (MW)':'Bioénergies (MW)'
    },
    axis=1
    )


# Tri par année
df_parc = df_parc.sort_values(by='Annee')
print(df_parc.dtypes)


# Ecriture du fichier modifié
df_parc.to_csv(
    path + '\\Data\\parc.csv', 
    sep=';', 
    index=False, 
    encoding='utf-8'
    )