# Librairies
import pandas as pd
import os


# Path
path = os.path.dirname(__file__)


# Lecture des fichiers RTE et météo
df_rte = pd.read_csv((path + '\\Data\\rte.csv'), sep = ';')
df_meteo = pd.read_csv((path + '\\Data\\weather_out.csv'), sep = ',')


# Conversion du champ 'Date' au format date
df_rte['Date'] = pd.to_datetime(df_rte['Date'])
df_meteo['aaaammjj'] = pd.to_datetime(df_meteo['aaaammjj'])


# Calcul de la plus haute consommation pour chaque jour
df_rte = df_rte.groupby(
    ['Annee', 'Mois', 'Date', 'Semaine', 'Jour_semaine', 'Heure', 'Date - Heure'],
    as_index=False).sum()

df_rte_max_jour = df_rte.loc[df_rte.groupby(
    ['Annee', 'Semaine', 'Date']
    )['Consommation (MW)'].idxmax()]


# Moyenne des températures par jour
df_meteo = df_meteo.groupby(
    ['aaaammjj', 'annee', 'mois'],
    as_index=False).mean()


# Croisement des fichiers
df_rte_meteo = df_rte_max_jour.merge(
    right=df_meteo,
    left_on=['Date'],
    right_on=['aaaammjj'],
    how='inner'
)

df_rte_meteo = df_rte_meteo.drop(
    ['Heure', 'Jour_semaine', 'Code INSEE région', 'Annee', 'Mois', 'aaaammjj', 'annee', 'joursem', 'jour', 'mois', 'region'],
    axis=1
)


# Date - Heure renommé 'Point_max' pour plus de clarté
## Correspond à l'heure avec le point de conso max sur la semaine
df_rte_meteo = df_rte_meteo.rename({'Date - Heure':'Point_max'}, axis=1)


# Création d'un df_rte_meteo_max_hebdo qui conserve le jour de chaque semaine
# avec la conso la plus élevée
df_rte_meteo_max_hebdo = df_rte_meteo.loc[df_rte_meteo.groupby(
    ['Semaine']
    )['Consommation (MW)'].idxmax()]

df_rte_meteo_max_hebdo = df_rte_meteo_max_hebdo.set_index('Semaine')


# Transformation de l'index du format semaine au format date
df_rte_meteo_max_hebdo['year'] = df_rte_meteo_max_hebdo.index.str[:4].astype(int)
df_rte_meteo_max_hebdo['week'] = df_rte_meteo_max_hebdo.index.str[-2:].astype(int)
dates = df_rte_meteo_max_hebdo['year']*100 + df_rte_meteo_max_hebdo['week']
df_rte_meteo_max_hebdo['Date'] = pd.to_datetime(dates.astype(str) + '0', format='%G%V%w')
df_rte_meteo_max_hebdo = df_rte_meteo_max_hebdo.set_index('Date')


# Ecriture du fichier de sortie
df_rte_meteo_max_hebdo.to_csv(
    path + '\\Data\\rte_meteo_max_hebdo.csv',
    sep=';'
)