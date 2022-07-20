# Librairies
import pandas as pd
import numpy as np
import os
import streamlit as st
from bokeh.plotting import figure
from bokeh.palettes import Category20
from bokeh.models import Legend
from statsmodels.tsa.arima_model import ARIMAResults


# @st.cache


# Path
path = os.path.dirname(__file__)


# Lecture fichiers
df_parc = pd.read_csv(
    path + '\\Data\\parc.csv', 
    sep=';',
    index_col='Annee'
)

df_rte_meteo = pd.read_csv(
    path + '\\Data\\rte_meteo_max_hebdo.csv',
    sep=';',
    decimal='.',
    index_col=['Date']
)


# Lecture du modèle de série temporelle
modele_conso = ARIMAResults.load(path + '\\conso_temp_st.pkl')


# Création de la séquence de température initiale
df_temp_initiales = df_rte_meteo.loc[df_rte_meteo.index>='2019-01', 'temp']


# Création df_data qui regroupera toutes les données
df_data = pd.DataFrame(
    columns=
    [
        'Thermique (MW)', 
        'Nucléaire (MW)', 
        'Eolien (MW)', 
        'Solaire (MW)', 
        'Hydraulique (MW)', 
        'Pompage (MW)', 
        'Bioénergies (MW)', 
        'Ech. physiques (MW)',
        'Production_totale'
    ]
)


# Paramétrage des blocs streamlit
sidebar = st.sidebar
viz = st.container()


# Lecture des niveaux de production min et max
thermique_max = int(df_parc.loc[2019]['Thermique (MW)'])
hydraulique_max = int(df_parc.loc[2019]['Hydraulique (MW)'])
nucleaire_max = int(df_parc.loc[2019]['Nucléaire (MW)'])
solaire_max = int(df_parc.loc[2019]['Solaire (MW)'])
eolien_max = int(df_parc.loc[2019]['Eolien (MW)'])
bioenergies_max = int(df_parc.loc[2019]['Bioénergies (MW)'])


# Paramétrage de la barre de menu
with sidebar:
    temperature_ecart = st.slider(
        'Ecart de température par rapport à la normale',
        min_value=-10,
        max_value=10,
        step=1,
        value=0
    )
    thermique = st.slider(
        'Production thermique',
        min_value=0,
        max_value=100,
        step=10,
        value=50
    ) / 100
    hydraulique = st.slider(
        'Production hydraulique', 
        min_value=0, 
        max_value=100, 
        step=10,
        value=50
    ) / 100
    nucleaire = st.slider(
        'Production nucléaire', 
        min_value=0, 
        max_value=100, 
        step=10,
        value=50
    ) / 100
    solaire = st.slider(
        'Production solaire', 
        min_value=0, 
        max_value=100, 
        step=10,
        value=50
    ) / 100
    eolien = st.slider(
        'Production éolienne', 
        min_value=0, 
        max_value=100, 
        step=10,
        value=50
    ) / 100
    bioenergies = st.slider(
        'Production bioénergies',
        min_value=0, 
        max_value=100, 
        step=10,
        value=50
    ) / 100
    ech_physiques = st.slider(
        'Echanges physiques disponibles',
        min_value=-10000,
        max_value=10000,
        step=1000,
        value=0
    )


# Calcul des niveaux de production en MW pour chaque filière
prod_thermique = int(thermique * thermique_max)
prod_hydraulique = int(hydraulique * hydraulique_max)
prod_nucleaire = int(nucleaire * nucleaire_max)
prod_solaire = int(solaire * solaire_max)
prod_eolien = int(eolien * eolien_max)
prod_bioenergies = int(bioenergies * bioenergies_max)


# Calcul des températures sélectionnées par l'utilisateur
df_temp_modif = df_temp_initiales + temperature_ecart


# Calcul de la consommation selon le modèle de série temporelle
df_previsions_conso_st = pd.DataFrame(
    modele_conso.forecast(
    52, 
    exog=df_temp_modif
    )
)
df_previsions_conso_st = df_previsions_conso_st.set_index(np.arange(0, 52, 1))


# Remplissage du df_data
production_totale = prod_thermique + prod_hydraulique + prod_nucleaire + prod_solaire + prod_eolien + prod_bioenergies + ech_physiques
df_data.loc[:, 'Consommation'] = df_previsions_conso_st
df_data.loc[:, 'Production_totale'] = production_totale
df_data['Production_utile'] = df_data[['Consommation','Production_totale']].min(axis=1)

nb_jours_tension = len(df_data[df_data['Consommation']>df_data['Production_totale']])

df_data['Thermique (MW)'] = prod_thermique
df_data['Hydraulique (MW)'] = prod_hydraulique
df_data['Nucléaire (MW)'] = prod_nucleaire
df_data['Solaire (MW)'] = prod_solaire
df_data['Eolien (MW)'] = prod_eolien
df_data['Bioénergies (MW)'] = prod_bioenergies
df_data['Ech. physiques (MW)'] = ech_physiques

# Bloc viz
with viz:

    if nb_jours_tension>0:
        toto = 'Au moins ' + str(nb_jours_tension) + ' jours de tension !'
        st.subheader(toto)

    p = figure(
        title='Titre',
        x_axis_label='Semaine',
        y_axis_label='MW'
    )


    # Graph customisation
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.ygrid.grid_line_dash = 'dotted'


    # Graph per country
    r1 = p.line(
        x='index',
        y='Consommation',
        source=df_data,
        line_alpha=0.9,
        line_width=2
    )

    r2 = p.line(
        x='index',
        y='Production_utile',
        source=df_data,
        line_alpha=0.9,
        line_dash='dashed',
        color='red',
        line_width=2
    )


    legend = Legend(items=[
    ("Consommation", [r1]),
    ("Production disponible", [r2]),
    ], location=(250, 450))

    p.add_layout(legend, 'center')

    st.bokeh_chart(p, use_container_width=True)


    # Affichage des données
    st.subheader('Détail des données')

    st.write(df_data)