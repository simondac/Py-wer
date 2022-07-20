# Packages
import streamlit as st
import pandas as pd
import numpy as np
#import os
from PIL import Image
from bokeh.plotting import figure
from bokeh.palettes import Category20
from bokeh.models import Legend
from statsmodels.tsa.arima_model import ARIMAResults


def leprojet ():
    image = Image.open('Images/electricite-gratuite.jpg')
    st.image(image, use_column_width= False)

    st.write("""
    # Pywer-generation

    Pywer-generation est un projet dont l'objectif est de prédire la
    consommation électrique et d'en déduire la tension possible sur
    le réseau français en fonction de paramètres de production choisis.
    Il est important de noter que la production d'électricité est basée sur
    les prévisions de consommation.
    
    Afin de rendre l'expérience utilisateur de ce streamlit plus 
    interactive, le dernier onglet permet de faire varier la consommation
    et la production de chaque filière (nucléaire, thermique, éolien, etc.)
    pour simuler la tension sur le réseau électrique en fonction des 
    paramètres entrés par l'utilisateur.
    """)

    st.subheader("Organisation de l'équipe")

    st.write("""
    Après quelques essais réalisés chacun de notre coté, nous avons décidé
    de nous partager le travail :   
    Chacun a pris un aspect particulier du problème afin de travailler 
    efficacement en parallèle. 
    C'est pour cette raison qu'il y a plusieurs fichiers ".py ou .ipynb" 
    dans le github du projet. 
    Ces "modules" génèrent parfois des fichiers qui sont réutilisés par le
    module suivant.
        
    Le diagrame ci-dessous décrit : 
    - l'organisation du code, 
    - Les fichiers open Data utilisés 
    - Les fichiers utilisés par le projet afin de faciliter le travail \
    commun mais aussi obtimiser l'espace mémoire utilisés
    - Les modèles générés
    """)

    im2 = Image.open('Images/Enchainement.jpg')
    st.image(im2, use_column_width=False)

    st.subheader("Données utilisées dans cette application")
    st.write("""
        La dernière étape du projet à consister dans la réalisation de ce 
        streamlit. Il reprend une partie des fichiers utilisés ou générés
         par le code décrit ci dessus.
         """)
    im3 = Image.open('Images/donnees_streamlit.PNG')
    st.image(im3, use_column_width=False)


    st.subheader("Liens utiles")

    st.write("**En rapport avec le projet**")
    link = '- Github projet :  https://github.com/DataScientest-Studio/Py-wer-Generation'
    st.markdown(link, unsafe_allow_html=True)

    st.write("**En rapport avec l'électricité de facon générale**")

    link = '- Le site de Rte : https://www.rte-france.com/'
    st.markdown(link, unsafe_allow_html=True)
    link2 = "- Nos données d'entrée en images : https://www.rte-france.com/eco2mix/la-consommation-delectricite-en-france"
    st.markdown(link2, unsafe_allow_html=True)
    link3 = '- Article : production nucléaire en france : https://www.edf.fr/groupe-edf/espaces-dedies/l-energie-de-a-a-z/tout-sur-l-energie/produire-de-l-electricite/le-nucleaire-en-chiffres#:~:text=Un%20r%C3%A9acteur%20de%20900%20MW,de%20400%20000%20foyers%20environ '
    st.markdown(link3, unsafe_allow_html=True)


def descriptiondesdonnées():
    st.header("Les données d'entrée")
    st.write("""
    Ce projet est basé sur 2 principaux ensemble de données que nous avons croisés :   
    * Les données de consommation et de production électrique par filière et par région à la maille quotidienne,  
    * Les données de climat (température, vitesse du vent, pluviométrie, nébulosité, quantité de neige... enregistrées à heure fixe toutes les 3 heures.
    Nous y avons ajouté des données de capacité de production maximale par filière pour étudier la tension sur le réseau électrique français.
    """)
    
    st.subheader("""1. Données de consommation/production électrique (extrait)""")
    pres_rte = pd.read_csv('Data/RTE_eco2mix_regional_cons_def_extrait.csv', sep=';', nrows=100)
    st.write(pres_rte)

    st.subheader("2. Données de climat (extrait)")
    pres_climat = pd.read_csv('Data/donnees-synop-essentielles-omm-extrait.csv', sep=';', nrows=100)
    st.write(pres_climat)

    st.subheader("3. Capacité de production maximale par filière et par année")
    df_parc = pd.read_csv('Data/parc-prod-par-filiere.csv', sep=';', nrows=100)
    st.write(df_parc)

    st.header("Les données additionnelles")
    st.write("""
    Deux autres sources de données ont été utilisées pour croiser nos données : les stations météo et la liste
    des communes françaises.
    """)

    st.subheader("1. Les stations météo")
    pres_station = pd.read_csv('Data/stations_meteo.csv', sep=';', nrows=100)
    st.write(pres_station)

    st.subheader("2. Les communes")
    pres_communes = pd.read_csv('data/communes2020.csv', sep=',', nrows=100)
    st.write(pres_communes)


    st.header("Transformation et croisement des données")

    st.write("""Afin de pouvoir joindre les données des 2 datasets RTE et météo, plusieurs opérations ont été réalisées sur
    chacun des fichiers.
    """)

    st.subheader("Transformation des données de consommation/production électrique")
    st.write ("""
    - Préparation des données : création de champs temporels, gestion des \
        valeurs manquantes
    - Création d'une colonne de production totale (somme de toutes les filières)
    - Agrégation des données (somme des données par région, et par jour ou \
        par mois, pour les besoins soit de l'exploration soit de la\
            modélisation).

    **Gestion des valeurs manquantes**
    - Les (premières) lignes du tableau ne comportant que des valeurs \
        manquantes ont été supprimées.
    - Les colonnes TCO/TCH (données de production relative par filière) ont\
        été supprimées car non utilisées par la suite.
    - Les valeurs manquantes ("NA") de production ont été remplacées par 0 \
        car elles correspondent à des régions qui ne comportent pas certaines \
            filières de production.

    **Fichiers de sortie**
    - Un DataFrame *rte* qui sera croisé avec les données météo
    - Un DataFrame *rte_jour_regions* utilisé pour l'exploration de données\
        et la modélisation en série temporelle.
    - Un DataFrame *rte_mois_regions* utilisé pour l'exploration de données \
        uniquement.
    """)

    st.subheader("Transformation des données de climat")
    st.write("Transformation des données de climat :"
     
       """***Sélection du périmètre*** :   
            Année : 2015 - 2019  
            Région : Afin de  trouver les régions et vérifier leur localisation, il a fallu :
            - faire le lien avec le fichier des stations 
            -  trouver la région de la station via le fichier des communes.  
       
       
       ***Gestion des Nan*** :   
            - Certaines colonnes comme le TCH et le TCO sont essentiellement vide et on du être supprimées. 
            - Concernant les colonnes significatives, il a fallu déterminer quelle était la meilleure facon de tranformer les nans :   
                   - Les précipitations : On considère que le Nan est équivalent à l'absence de pluie. On a remplacer les NAN par 0.
                   - Les données de températures,  Humidité, vitesse moyenne  : Nous avons calculé la valeur manquante en faisant la moyenne de la ligne précédente et la ligne suivante sur une dataframe triée correctement.  
                   - Les données de nébulosité : Avant de calculer les moyennes comme pour les autres mesure, les périodes correspondant à la nuit ont été mise à 100 (la nuit il fait ... nuit ).  

       ***Agregation à la journée*** 
       Afin de pouvoir joindre les données de consommation et les données de climat il fallait que les deux soient sur les mêmes niveaux d'agrégats.  
       Nous avons donc agréger les données de climat à la journée""")
    
    st.write("""***Données du streamlit : Limite***    
       
    Comme nous le verrons plus tard, nous avons utilisé les données de nébulosité  et de température pour prédire la production d'énergie solaire.    
    Hors la nébulosité correspond à la fraction de la voute céleste occultée par les nuages au moment de l’évaluation (wikipédia).   
    Ce n'est pas la mesure que l'on devrait utiliser afin d'obtenir un modèle très performant mais l'ensoleillement. 
    Cette mesure n'est pas disponible de facon gratuite à part à l'année""")

    st.subheader("Croisement des données")
    st.write("""
    Nous avons croisé les données RTE et météo selon les critères suivants :
    - Pour chaque semaine, conservation du point demi-horaire ayant la plus \
    forte consommation au niveau national.
    - Pour les données de production par filière : conservation des données \
    pour le point demi-horaire précédemment conservé chaque semaine.
    - Moyenne des températures au niveau national pour chaque jour.
    En sortie est généré un DataFrame *rte_meteo_max_hebdo*.

    *Note : un fichier équivalent a également été créé, mais avec une \
        agrégation par région, pour les besoins de la modélisation de la \
            production éolienne.*
    """)


def explorationdesdonnées():
    st.header("Exploration des données")

    st.write ("L'objectif de cette étape est de comprendre les données que \
        nous allons manipuler")

    st.subheader('Niveaux relatifs de consommation et de production')
    
    col1, mid, col2 = st.columns([20, 2, 20])

    with col1:
        st.image(
            'Data\Screenshots_EDA\carte_conso.jpg',
            output_format='JPEG',
            use_column_width='auto',
            # width=300,
            caption='Niveau de consommation relative entre régions'
            )

    with col2:
        st.image(
            'Data\Screenshots_EDA\carte_production.jpg',
            output_format='JPEG',
            use_column_width='auto',
            # width=300,
            caption='Niveau de production relative entre régions'
            )

    st.subheader('Consommation par jour de la semaine')
    st.image('Data\Screenshots_EDA\conso_jour_semaine.jpg',
            output_format='JPEG',
            use_column_width='auto',
            caption='Consommation moyenne par jour de la semaine \
                selon les années'
            )

    st.subheader('Empilement des productions par filière')
    st.image('Data\Screenshots_EDA\prod_filiere_2019.jpg',
            output_format='JPEG',
            use_column_width='auto',
            caption="Production quotidienne (MWh) pour chaque filière, \
                pour l'année 2019 prise comme exemple"
            )

    st.subheader('Productions mensuelles pour chaque filière')
    st.image('Data\\Screenshots_EDA\\filiere_mensuel.png',
            output_format='PNG',
            use_column_width='auto',
            caption="Production mensuelle (MWh) pour chaque filière, \
                pour l'année 2019 prise comme exemple"
            )

    st.subheader('Consommation en fonction de la température')
    st.image('Data\\Screenshots_EDA\\conso_temperature_region_11.png',
            output_format='PNG',
            use_column_width='auto',
            caption="Consommation (MWh) expliquée par la température, pour la \
                région Ile-de-France (consommation journalière et \
                    température moyenne journalière)"
            )

    st.subheader('Production éolienne en fonction de la vitesse du vent')
    st.image('Data\\Screenshots_EDA\\vitesse_vent_prod_eolienne_region_32.png',
            output_format='PNG',
            use_column_width='auto',
            caption="Production éolienne (MWh) expliquée par la vitesse du \
                vent, pour la région Ile-de-France (Production journalière et \
                    vitesse du vent moyenne journalière)"
                    )

def letsplay():
    # Path
    #path = os.path.dirname(__file__)


    # Lecture fichiers
    df_parc = pd.read_csv(
        path + 'Data\parc.csv', 
        sep=';',
        index_col='Annee'
    )

    df_rte_meteo = pd.read_csv(
        'Data\rte_meteo_max_hebdo.csv',
        sep=';',
        decimal='.',
        index_col=['Date']
    )

    df_predictions_vent = pd.read_csv(
        'Data\predictions_vent.csv',
        sep=';',
        decimal='.',
        # index_col=['Date']
    )


    # Lecture du modèle de série temporelle
    modele_conso = ARIMAResults.load('Modeles\conso_temp_st.pkl')


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
        param_temperature = st.slider(
            'Ecart de température (*modèle*)',
            min_value=-10,
            max_value=10,
            step=1,
            value=0
        )
        param_eolien = st.select_slider(
            'Production éolienne (*modèle*)', 
            options=['Vent minimum', 'Vent faible', 'Vent moyen', 'Vent fort', 'Vent maximum'], 
            value=('Vent moyen')
        )
        thermique = st.slider(
            'Production thermique (% du max)',
            min_value=0,
            max_value=100,
            step=10,
            value=50
        ) / 100
        hydraulique = st.slider(
            'Production hydraulique (% du max)', 
            min_value=0, 
            max_value=100, 
            step=10,
            value=50
        ) / 100
        nucleaire = st.slider(
            'Production nucléaire (% du max)', 
            min_value=0, 
            max_value=100, 
            step=10,
            value=50
        ) / 100
        solaire = st.slider(
            'Production solaire (% du max)', 
            min_value=0, 
            max_value=100, 
            step=10,
            value=50
        ) / 100
        bioenergies = st.slider(
            'Production bioénergies (% du max)',
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
    prod_eolien = int(df_predictions_vent[param_eolien][0])
    prod_bioenergies = int(bioenergies * bioenergies_max)


    # Calcul des températures sélectionnées par l'utilisateur
    df_temp_modif = df_temp_initiales + param_temperature


    # Calcul de la consommation selon le modèle de série temporelle
    df_previsions_conso_st = pd.DataFrame(
        modele_conso.forecast(
        52, 
        exog=df_temp_modif
        )
    )
    df_previsions_conso_st = df_previsions_conso_st.set_index(np.arange(0, 52, 1))


    # Remplissage du df_data
    # production_totale = prod_thermique + prod_hydraulique + prod_nucleaire \
    #     + prod_solaire + prod_eolien + prod_bioenergies + ech_physiques
    df_data.loc[:, 'Consommation'] = df_previsions_conso_st
    # df_data.loc[:, 'Production_totale'] = production_totale
    # df_data['Production_utile'] = df_data[['Consommation','Production_totale']].min(axis=1)

    # nb_jours_tension = len(df_data[df_data['Consommation']>df_data['Production_totale']])

    df_data['Thermique (MW)'] = prod_thermique
    df_data['Hydraulique (MW)'] = prod_hydraulique
    df_data['Nucléaire (MW)'] = prod_nucleaire
    df_data['Solaire (MW)'] = prod_solaire
    df_data['Eolien (MW)'] = df_predictions_vent[param_eolien].astype(int)
    df_data['Bioénergies (MW)'] = prod_bioenergies
    df_data['Ech. physiques (MW)'] = ech_physiques
    df_data.loc[:, 'Production_totale'] = df_data['Thermique (MW)'] \
        +df_data['Hydraulique (MW)'] \
        +df_data['Nucléaire (MW)'] \
        +df_data['Solaire (MW)'] \
        +df_data['Eolien (MW)'] \
        +df_data['Bioénergies (MW)'] \
        +df_data['Ech. physiques (MW)']
    df_data['Production_utile'] = df_data[['Consommation','Production_totale']].min(axis=1)

    nb_jours_tension = len(df_data[df_data['Consommation']>df_data['Production_totale']])


    # Bloc viz
    with viz:
        if nb_jours_tension>0:
            toto = 'Au moins ' + str(nb_jours_tension) + " jours de tension pendant l'année !"
            st.subheader(toto)

        p = figure(
            x_axis_label='Semaine',
            y_axis_label='Production (MW)'
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

st.set_page_config (layout = "centered") #, menu_items = {'About': "# This is a header. This is an *extremely* cool app!"})

with st.sidebar:
    add_radio = st.radio(
        "Pywer-generator",
        ("Le projet", "Les données et leur transformation", "EDA", "Modélisation", "Let's play !")
    )
if add_radio == 'Le projet':
    leprojet()

if add_radio == "Les données et leur transformation":
    descriptiondesdonnées()

if add_radio == "EDA":
    explorationdesdonnées()

if add_radio == "Let's play !":
    letsplay()
