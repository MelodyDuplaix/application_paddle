import streamlit as st
import pandas as pd
from bibliotheque.lib import  *
from st_pages import Page, show_pages, add_page_title, Section
from datetime import datetime 
from plotly.offline import iplot
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import sqlite3
from datetime import datetime
from PIL import Image


# Définition des fonctions


def creation_base_et_table():
    """
    Nom : creation_base_et_table
    Paramètres : 0
    Traitement : crée la base et les 2 tables salariés et villes si elles n'existent pas
    Retour : rien
    """
    connexion = sqlite3.connect("data/personnel_societe_paddle")
    cursor = connexion.cursor()
    table_salaries = """ 
                    CREATE TABLE IF NOT EXISTS salaries(
                    id_salarie INTEGER PRIMARY KEY,
                    prenom VARCHAR(50) NOT NULL,
                    nom_sa VARCHAR(50) NOT NULL,
                    mail VARCHAR(100) NOT NULL,
                    genre VARCHAR(10) NOT NULL,
                    date_naissance DATE NOT NULL,
                    date_arrivee DATE NOT NULL,
                    id_ville SMALLINT NOT NULL,
                    date_sortie DATE,
                    FOREIGN KEY(id_ville) REFERENCES villes(id_ville)
                    );
                    """
    table_villes = """
                    CREATE TABLE IF NOT EXISTS villes(
                    id_ville INTEGER PRIMARY KEY,
                    nom_ville VARCHAR(80) NOT NULL
                    );
                    """
    cursor.execute(table_salaries)
    cursor.execute(table_villes)
    connexion.commit()
    connexion.close()

def calcul_ages():
    """
    Nom : calcul_ages
    Paramètres : 0
    Traitement : récupère la table entière et calcule les âges
    Retour : un dataFrame
    """
    dataset = récupération_dataset_total()
    dataset["date_naissance"] = pd.to_datetime(dataset["date_naissance"])
    today = datetime.now()
    dataset["age"]=today - dataset["date_naissance"]
    dataset["age"] = dataset["age"] / pd.Timedelta(days=365)
    return(dataset)
    
def groupement_ages():
    """
    Nom : calcul_ages
    Paramètres : 0
    Traitement : calcule le nombre de personnes par tranche d'âges
    Retour : un dataFrame
    """
    dataset = calcul_ages()
    bins = [17, 30, 40, 50, 60, float('inf')]
    labels = ['17-29', '30-39', '40-49', '50-60', "60+"]
    dataset["tranche_age"] = pd.cut(dataset["age"], bins=bins, labels=labels)
    dataset = dataset.groupby("tranche_age").size().reset_index(name="nombre")
    return(dataset)

def graph_age(f_dataset_age):
    """
    Nom : graph_age
    Paramètres : 1, dataFrame
    Traitement : construit le graphique du nombre par tranches d'âges
    Retour : un graphique
    """
    graph_tranche_age = px.pie(f_dataset_age, names="tranche_age", values="nombre", color="tranche_age", color_discrete_map={
        '60+':'#004484',
        '50-60':'#005fb8',
        '40-49':'#0072de',
        '30-39':'#5db1ff',
        '17-29':'#c3e2ff'
    },category_orders={"tranche_age":["17-29","30-39","40-49","50-60","60+"]})
    graph_tranche_age.update_traces(hovertemplate="%{label} : %{value}")
    return(graph_tranche_age)

def calcul_total():
    """
    Nom : calcul_total
    Paramètres : 0
    Traitement : récupère le nombre de salariés total
    Retour : un nombre
    """
    connexion = sqlite3.connect("data/personnel_societe_paddle")
    cursor = connexion.cursor()
    TABLE_TOTAL = """ 
                    SELECT COUNT(*)
                    FROM salaries;
                """
    cursor.execute(TABLE_TOTAL)
    nombre_total = cursor.fetchone()
    connexion.close()
    return(nombre_total)

def calcul_genres():
    """
    Nom : calcul_genres
    Paramètres : 0
    Traitement : récupère le nombre de salariés par genre
    Retour : un dataFrame
    """
    connexion = sqlite3.connect("data/personnel_societe_paddle")
    cursor = connexion.cursor()
    groupement_ville = """ 
                    SELECT genre, COUNT(*) AS nombre_de_salariés
                    FROM salaries
                    GROUP BY genre
                    ORDER BY nombre_de_salariés
                """
    cursor.execute(groupement_ville)
    dataset_genre = pd.DataFrame(cursor.fetchall(), columns=["genre","nombre"])
    connexion.close()
    return(dataset_genre)
    
def graph_genres(f_dataset_genre):
    """
    Nom : graph_genres
    Paramètres : 1 , dataFrame
    Traitement : construit un graphique du nombre par genre
    Retour : un graphique
    """
    graph_genre = px.pie(f_dataset_genre, names="genre", values="nombre", color="genre", color_discrete_map={
        'F':'orange',
        'M':'purple'
    })
    graph_genre.update_traces(hovertemplate="%{label} : %{value}")
    return(graph_genre)

def calcul_villes():
    """
    Nom : calcul_villes
    Paramètres : 0
    Traitement : récupère le nombre de salariés par ville
    Retour : un dataFrame
    """
    connexion = sqlite3.connect("data/personnel_societe_paddle")
    cursor = connexion.cursor()
    groupement_ville = """ 
                    SELECT v.nom_ville, COUNT(*) AS nombre_de_salariés
                    FROM salaries AS s
                    JOIN villes AS v
                    ON s.id_ville = v.id_ville
                    GROUP BY v.id_ville, v.nom_ville
                    ORDER BY v.id_ville;
                """
    cursor.execute(groupement_ville)
    dataset_ville = pd.DataFrame(cursor.fetchall(), columns=["nom_ville","nombre"])
    connexion.close()
    return(dataset_ville)

def graph_villes(f_dataset_villes):
    """
    Nom : graph_villes
    Paramètres : 1, dataFrame
    Traitement : construit le graphique du nombre par nom_ville
    Retour : un graphique
    """
    graph_ville = px.pie(f_dataset_villes, names="nom_ville", values="nombre", color="nom_ville", color_discrete_sequence=px.colors.qualitative.Vivid_r)
    graph_ville.update_traces(hovertemplate="%{label} : %{value}")
    return(graph_ville)

@st.cache_data
def récupération_dataset_total():
    """
    Nom : récupération_dataset_total
    Paramètres : 0
    Traitement : récupère l'ensemble de la table salariés lié à la table ville
    Retour : un dataFrame
    """
    liste_colonnes = ["id", "prenom", "nom_sa","mail","genre","date_naissance","date_arrivee","date_sortie","nom_ville"]
    connexion = sqlite3.connect("data/personnel_societe_paddle")
    cursor = connexion.cursor()
    TABLE_TOTAL = """ 
                    SELECT id_salarie , prenom, nom_sa, mail, genre , date_naissance , date_arrivee , date_sortie, villes.nom_ville
                    FROM salaries
                    JOIN villes
                    ON salaries.id_ville = villes.id_ville;
                """
    cursor.execute(TABLE_TOTAL)
    dataset = pd.DataFrame(cursor.fetchall(),columns=liste_colonnes)
    connexion.close()
    return(dataset)

def récupérer_liste_ville():
    """
    Nom : récupérer_liste_ville
    Paramètres : 0
    Traitement : récupère l'ensemble des villes dans la table villes
    Retour : une liste
    """
    connexion = sqlite3.connect("data/personnel_societe_paddle")
    cursor = connexion.cursor()
    TABLE_TOTAL = """ 
                    SELECT DISTINCT(nom_ville)
                    FROM villes;
                """
    cursor.execute(TABLE_TOTAL)
    liste_villes = [row[0] for row in cursor.fetchall()]
    connexion.close()
    return(liste_villes)

@st.cache_data
def récupérer_tableau_ville():
    """
    Nom : récupérer_liste_ville
    Paramètres : 0
    Traitement : récupère l'ensemble des villes dans la table villes
    Retour : une liste
    """
    connexion = sqlite3.connect("data/personnel_societe_paddle")
    cursor = connexion.cursor()
    TABLE_VILLE_TOTAL = """ 
                    SELECT *
                    FROM villes;
                """
    cursor.execute(TABLE_VILLE_TOTAL)
    liste_villes = pd.DataFrame(cursor.fetchall(), columns=["id","nom"])
    connexion.close()
    return(liste_villes)

def sidebar():
    """
    Nom : sidebar
    Paramètres : 0
    Traitement : configures les pages de la sidebar
    Retour : un affichage
    """
    show_pages(
        [
            Page("acceuil.py", "Home", "🏠"),
            Page("Pages/afficher.py", "Afficher les salariés"),
            Page("Pages/ajouter.py", "Ajouter des salariés"),
            Page("Pages/modifier.py", "Modifier les salariés"),
            Page("Pages/supprimer.py", "Supprimer des salariés"),
            Page("Pages/rgpd.py", "RGPD"),
            Page("Pages/mentions_legales.py", "Mentions Légales")
        ]
    )
    st.sidebar.title("Menu")

def header_avec_image(f_titre, f_contexte):
    """
    Nom : header_avec_image
    Paramètres : 2, 1-chaine de caractère, 2-chaine de caractère
    Traitement : crée un header avec une image, un titre, et un contexte
    Retour : un affichage
    """
    colonne_logo, colonne_titre = st.columns([1,5])
    with colonne_logo:
        logo = Image.open("images/photoprofillinkedIn.excalidraw.png")
        logo_reduit = logo.resize([70,50])
        st.image(logo_reduit)
    with colonne_titre:
        st.title(f_titre)
    st.write(f_contexte)
    st.write()

def header(f_titre, f_contexte):
    """
    Nom : header
    Paramètres : 2, 1-chaine de caractère, 2-chaine de caractère
    Traitement : crée un header avec un titre, et un contexte
    Retour : un affichage
    """
    colonne_logo, colonne_titre = st.columns([1,5])
    with colonne_logo:
        st.write("")
    with colonne_titre:
        st.title(f_titre)
    st.write(f_contexte)
    st.write()

def formatage_de_la_page(f_fichier_css):
    """
    Nom : formatage_de_la_page
    Paramètres : 1 chaine de caractère
    Traitement : prend un fichier css et applique le style
    Retour : un affichage
    """
    with open(f_fichier_css) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

def config_site(f_layout):
    """
    Nom : config_site
    Paramètres : 1 chaine de caractère
    Traitement : configure les options de la page, avec le layout choisi ("wide" ou "centered")
    Retour : un affichage
    """
    st.set_page_config(
        page_title="Analyse associations",
        page_icon="📊",
        layout=f_layout,
        menu_items={
            "Get Help": "https://www.cefim.eu/",
            "About" : "https://www.linkedin.com/in/melody-duplaix-391672265"
        }
    )
    formatage_de_la_page("style.css")

@st.cache_data
def footer():
    """
    Nom : footer
    Paramètres : 0
    Traitement : crée un footer avec les deux liens vers RGPD et mentions légales
    Retour : un affichage
    """
    footer1 = "<a href='Mentions Légales' target='_self' class='link' text-align='center'>Mentions légales</a> " 
    footer2 = "<a href='RGPD' target= '_self' class='link' text-align='center'>RGPD</a> "
    col1, col2 = st.columns(2)
    with col1:
        st.write(footer1, unsafe_allow_html=True)
    with col2:
        st.write(footer2, unsafe_allow_html=True)
  
  

