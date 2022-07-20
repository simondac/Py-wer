import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image


def leprojet ():
    image = Image.open('electricite-gratuite.jpg')
    st.image(image, use_column_width= False)

    st.write("""
        # Pywer-generation

        Pywer-generation est un projet dont l'objectif est de prédire la consommation électrique.  
        Il est important de noter que la production d'électricité en france est basée sur les estimations de consommation.
        
        Afin de rendre l'expérience utilisateur de ce streamlit plus interactive, le dernier onglet permet de modifier les paramètres de production des énérgies vertes et nucleaires afin de simuler l'impact sur la production.   

        ***Organisation de l'équipe***    

         Après quelques essais réalisés chacun de notre coté, nous avons décidé de nous partager le travail :   
         Chacun a pris un aspect particulier du problème afin de travailler efficacement en parallèle. 
         C'est pour cette raison qu'il y a plusieurs fichiers ".py ou .ipynb" dans le github du projet. 
         Ces "modules" génèrent parfois des fichiers qui sont réutilisés par le module suivant.
         
         Le diagrame ci dessous décrit : 
         - l'organisation du code, 
         - Les fichiers open Data utilisés 
         - Les fichiers utilisés par le projet afin de faciliter le travail commun mais aussi obtimiser l'espace mémoire utilisés
         - Les modèles générés""")

    im2 = Image.open('Organisation_du_code.PNG')
    st.image(im2, use_column_width=False)


    st.write("""
          ***Données utilisées dans ce streamlit***   
             
           La dernière étape du projet à consister dans la réalisation de ce streamlit. Il reprend une partie des fichiers utilisés ou générés par le code décrit ci dessus. """)
    im3 = Image.open('Données utilisées dans le Streamlit.PNG')
    st.image(im3, use_column_width=False)


    st.write("""   ***Liens utiles***""")

    st.write("""    - En rapport avec le projet """)
    link = 'Github projet :  https://github.com/DataScientest-Studio/Py-wer-Generation'
    st.markdown(link, unsafe_allow_html=True)

    st.write("""    En rapport avec l'électricité de facon générale """)

    link = 'Le site de Rte  :  https://www.rte-france.com/'
    st.markdown(link, unsafe_allow_html=True)
    link2 = 'Nos données en images https://www.rte-france.com/eco2mix/la-consommation-delectricite-en-france'
    st.markdown(link2, unsafe_allow_html=True)
    link3 = 'Article : production nucléaire en france: https://www.edf.fr/groupe-edf/espaces-dedies/l-energie-de-a-a-z/tout-sur-l-energie/produire-de-l-electricite/le-nucleaire-en-chiffres#:~:text=Un%20r%C3%A9acteur%20de%20900%20MW,de%20400%20000%20foyers%20environ '
    st.markdown(link3, unsafe_allow_html=True)


def descriptiondesdonnées():



    st.header(""" Les données  """)
    st.write("""
    Ce projet est basé sur 2 ensembles de données que nous avons mis en cohérence :   
    * Les données de consommation et de production électrique par filière et par région à la maille quotidienne,  
    * Les données de climat (température, vitesse du vent, pluviométrie, nébulosité,quantité de neige ... enregistrées à heure fixe toutes les 4 heures..
    * Les données de capacité maximale par filière. """)
    st.subheader("""Données de consommation/production électrique""")
    pres_rte = pd.read_csv('./data/df_rte.csv', sep=';', nrows=100)
    st.write("""   
            """)
    st.write(pres_rte)

    st.subheader("""Données de climats""")
    pres_climat = pd.read_csv('data/eco2mix-regional-cons-def.csv', sep=';', nrows=100)
    st.write("""   
          """)
    st.write(pres_climat)

    st.subheader("""Les stations météo""")
    pres_station = pd.read_csv('data/stations_meteo.csv', sep=';', nrows=100)
    st.write("""   
             """)
    st.write(pres_station)

    st.subheader("""Les communes""")
    pres_communes = pd.read_csv('data/communes2020.csv', sep=',', nrows=100)
    st.write("""   
                """)
    st.write(pres_communes)

    st.subheader("""Capacité maximale par filière""")

    st.write("""  MANQUE LE FICHIER EN ENTREE DANS /data  
              """)
    st.header("""Transformation et mise en commun des données""")

    st.write(""" 
    Afin des pouvoir joindre les données des 2 datasets, plusieurs opérations ont été réalisées sur les fichiers : 
     
      
      """)
    st.subheader("""Transformation des données de consommation/production électrique :""")
    st.write ("""      BLABLABLA""")
    st.subheader("""Transformation des données de climat :""")
    st.write(""" Transformation des données de climat :    
     
       ***Sélection du périmètre*** :   
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
       Nous avons donc agréger les données de climat à la journée
       """   )
    
    st.write(""" ***Données du streamlit : Limite***    
       
    Comme nous le verrons plus tard, nous avons utilisé les données de nébulosité  et de température pour prédire la production d'énergie solaire.    
    Hors la nébulosité correspond à la fraction de la voute céleste occultée par les nuages au moment de l’évaluation (wikipédia).   
    Ce n'est pas la mesure que l'on devrait utiliser afin d'obtenir un modèle très performant mais l'ensoleillement. 
    Cette mesure n'est pas disponible de facon gratuite à part à l'année"""   )



def explorationdesdonnées():
    st.header(""" Exploration des données  """)

    st.write (""" L'objectif de cette étape est de comprendre les données que nous allons manipuler""")

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
            caption="Production quotidienne pour chaque filière, \
                pour l'année 2019 prise comme exemple"
            )

    st.subheader('Productions mensuelles pour chaque filière')
    st.image('Data\\Screenshots_EDA\\filiere_mensuel.png',
            output_format='PNG',
            use_column_width='auto',
            caption="Production mensuelle pour chaque filière, \
                pour l'année 2019 prise comme exemple"
            )

    st.subheader('Consommation en fonction de la température')
    st.image('Data\\Screenshots_EDA\\conso_temperature_region_11.png',
            output_format='PNG',
            use_column_width='auto',
            caption="Régression linéaire de la consommation expliquée \
                par la température, pour une région française prise au hasard"
            )

    st.subheader('Production éolienne en fonction de la vitesse du vent')
    st.image('Data\\Screenshots_EDA\\vitesse_vent_prod_eolienne_region_32.png',
            output_format='PNG',
            use_column_width='auto',
            caption="Régression linéaire de la production éolienne expliquée \
                par la vitesse du vent, pour une région française \
                    prise au hasard"
            )

    # df_rte = pd.read_csv('df_rte.csv', sep=';')
    # df_climat = pd.read_csv('weather_out.csv', sep=';')
    # st.write ("""Production et consommation en france
    #           ICI """
    #           )
    # annee = 2019

    # st.subheader("""   
       
    #     ***Productions journalières empilées par filière (année 2019)***
    #  """
    #          )
    # fig = plt.figure(figsize=(12,8 ))

    # myplot = fig.add_subplot(111)

    # data = df_rte[df_rte['Annee'] == annee].groupby('Date', as_index=False).agg(sum)

    # data[['Date',
    # 'Thermique (MW)',
    # 'Nucléaire (MW)',
    # 'Eolien (MW)',
    # 'Solaire (MW)',
    # 'Bioénergies (MW)',
    # 'Hydraulique (MW)',]].plot.area(ax= myplot,x='Date', stacked = False
    #                )
    # fig

    # st.write (""" La majorité de la production provient de la filière nucléaire. La consommation d'électricité est nettement plus faible en été qu'en hiver. """)
#    data = plt.stackplot(
    #        'Date',
    #    'Thermique (MW)',
    #     'Nucléaire (MW)',
    #    'Eolien (MW)',
    #    'Solaire (MW)',
    #    'Bioénergies (MW)',
    #    'Hydraulique (MW)',
    #    data=data,
    #    labels=['Thermique', 'Nucléaire', 'Eolien', 'Solaire', 'Bioénergies', 'Hydraulique'],
    #    colors=['brown', 'orange', 'green', 'yellow', 'grey', 'blue']
    #)
    #plt.ylabel('Puissance (MW)')
    #plt.xticks([str(annee) + '-01-01', str(annee) + '-04-01', str(annee) + '-07-01', str(annee) + '-10-01'])
    #plt.title('Production par filière en ' + str(annee))
    #plt.legend(loc='upper center');





st.set_page_config (layout = "centered", menu_items = {'About': "# This is a header. This is an *extremely* cool app!"}
                    )

with st.sidebar:
    add_radio = st.radio(
        "Pywer-generator",
        ('Le projet',"Les données et leur transformation","EDA","Modélisation","Let's play !")
    )
if add_radio == 'Le projet':
    leprojet()

if add_radio == "Les données et leur transformation":
    descriptiondesdonnées()

if add_radio == "EDA":
    explorationdesdonnées()