# Import des bibliothèques
import streamlit as st
from PIL import Image
import pandas as pd
from bibliotheque.lib import  *
from st_pages import Page, show_pages, add_page_title
import numpy as np
import sqlite3
import datetime

config_site("wide")
sidebar()


# titre, contexte et logos
header("Tableau de modification des salariés","")




# Code principal

# Récupération des salariés
dataset = récupération_dataset_total()
dataset["identifiant"] = dataset["prenom"] + " " + dataset["nom_sa"]
liste_nom = dataset["identifiant"].to_list()
dataset["date_naissance"] = pd.to_datetime(dataset['date_naissance'])
dataset["date_arrivee"] = pd.to_datetime(dataset['date_arrivee'])
dataset["date_sortie"] = pd.to_datetime(dataset['date_sortie'])

dataset_modifie = st.data_editor(dataset, hide_index=True, width=14000, column_config={
    "id":"id",
    "prenom":"prenom",
    "nom_sa":"nom",
    "mail":"mail",
    "genre":"genre",
    "date_naissance":st.column_config.DateColumn(
        "date de naissance", format="DD/MM/YYYY", required=True
        ),
    "date_arrivee":st.column_config.DateColumn(
        "date de date_arrivee", format="DD/MM/YYYY",required=True
        ),
    "date_sortie":st.column_config.DateColumn(
        "date de sortie", format="DD/MM/YYYY",required=True
        ),
    "nom_ville":"ville de travail",
    "identifiant":None
})


footer()