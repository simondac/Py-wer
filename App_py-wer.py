# Librairies
import pandas as pd
import numpy as np
import os
import streamlit as st
from bokeh.plotting import figure
from bokeh.palettes import Category20
from bokeh.models import Legend


# @st.cache


# Path
path = os.path.dirname(__file__)


# Lecture fichiers
df_production = pd.read_csv(
    path + '\\df_production.csv', 
    sep=';', 
    index_col='Semaine'
    )

df_parc = pd.read_csv(
    path + '\\df_parc.csv', 
    sep=';',
    index_col='Annee'
    )   

df_previsions_conso = pd.read_csv(
    path + '\\previsions_conso_ST.csv', 
    sep=';'
    )


# Filtre du df_previsions_conso
df_previsions_conso = df_previsions_conso[(df_previsions_conso['Semaine']>='2020-01') & (df_previsions_conso['Semaine']<='2020-53')]
df_previsions_conso = df_previsions_conso.set_index(np.arange(0, len(df_previsions_conso), 1))


# Création df df_production_calculee
df_production_selectionnee = pd.DataFrame(
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
    # index=df_previsions_conso['Semaine']
    )


# Lecture des semaines min et max
liste_semaines = df_production.index.unique()


# Paramétrage des blocs streamlit
sidebar = st.sidebar
viz = st.container()


# Lecture des niveaux de production min et max
thermique_max = int(df_parc.loc[2020]['Thermique (MW)'])
hydraulique_max = int(df_parc.loc[2020]['Hydraulique (MW)'])
nucleaire_max = int(df_parc.loc[2020]['Nucléaire (MW)'])
solaire_max = int(df_parc.loc[2020]['Solaire (MW)'])
eolien_max = int(df_parc.loc[2020]['Eolien (MW)'])
bioenergies_max = int(df_parc.loc[2020]['Bioénergies (MW)'])


with sidebar:
    thermique = st.slider('Production thermique', min_value=0.0, max_value=1.0, step=0.1)
    hydraulique = st.slider('Production hydraulique', min_value=0.0, max_value=1.0, step=0.1)
    nucleaire = st.slider('Production nucléaire', min_value=0.0, max_value=1.0, step=0.1)
    solaire = st.slider('Production solaire', min_value=0.0, max_value=1.0, step=0.1)
    eolien = st.slider('Production éolienne', min_value=0.0, max_value=1.0, step=0.1)
    bioenergies = st.slider('Production bioénergies', min_value=0.0, max_value=1.0, step=0.1)
    ech_physiques = st.slider('Echanges physiques disponibles', min_value=-10000, max_value=10000, step=1000)


# Calcul des niveaux de production en MW pour chaque filière
thermique_prod = int(thermique * thermique_max)
hydraulique_prod = int(hydraulique * hydraulique_max)
nucleaire_prod = int(nucleaire * nucleaire_max)
solaire_prod = int(solaire * solaire_max)
eolien_prod = int(eolien * eolien_max)
bioenergies_prod = int(bioenergies * bioenergies_max)


# Remplissage du df_production_selectionnee
production_totale = thermique_prod + hydraulique_prod + nucleaire_prod + solaire_prod + eolien_prod + bioenergies_prod + ech_physiques
df_production_selectionnee.loc[:, 'Consommation'] = df_previsions_conso['predicted_mean'].values
df_production_selectionnee.loc[:, 'Production_totale'] = production_totale
consommation = df_production_selectionnee['Consommation'].values
df_production_selectionnee['Production_utilisee'] = df_production_selectionnee[['Consommation','Production_totale']].min(axis=1)
nb_jours_tension = len(df_production_selectionnee[df_production_selectionnee['Consommation']>df_production_selectionnee['Production_totale']])

df_production_selectionnee['Thermique (MW)'] = thermique_prod
df_production_selectionnee['Hydraulique (MW)'] = hydraulique_prod
df_production_selectionnee['Nucléaire (MW)'] = nucleaire_prod
df_production_selectionnee['Solaire (MW)'] = solaire_prod
df_production_selectionnee['Eolien (MW)'] = eolien_prod
df_production_selectionnee['Bioénergies (MW)'] = bioenergies_prod
df_production_selectionnee['Ech. physiques (MW)'] = ech_physiques


# Bloc viz
with viz:

    st.write(str(nb_jours_tension), ' semaines de tension !')
    p = figure(
        title='Titre',
        x_axis_label='Semaine',
        y_axis_label='MW'
        )


    # Graph customisation
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_dash = 'dotted'


    # Graph per country
    r1 = p.line(
        x='index',
        y='Consommation',
        source=df_production_selectionnee,
        line_alpha=0.9,
        # legend_label='Consommation',
        line_width=2
        )

    r2 = p.line(
        x='index',
        y='Production_utilisee',
        source=df_production_selectionnee,
        line_alpha=0.9,
        line_dash='dashed',
        color='red',
        # legend_label='Production',
        line_width=2
        )

    legend = Legend(items=[
    ("Consommation",   [r1]),
    ("Production", [r2]),
    ], location=(250, 450))

    p.add_layout(legend, 'center')

    st.bokeh_chart(p, use_container_width=True)

    st.write(df_production_selectionnee)
