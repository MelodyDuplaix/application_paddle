# Import des bibliothèques
import streamlit as st
from PIL import Image
import pandas as pd
from bibliotheque.lib import  *
from st_pages import Page, show_pages, add_page_title
from datetime import datetime 
import numpy as np
import sqlite3
from datetime import datetime

config_site("wide")
sidebar()


# titre, contexte et logos
header("Formulaire de suppression de salariés","")




# Code principal

# Récupération des salariés
dataset = récupération_dataset_total()
dataset["identifiant"] = dataset["prenom"] + " " + dataset["nom_sa"]
liste_nom = dataset["identifiant"].to_list()

# Création du choix

dataset_id = pd.DataFrame()
with st.form("suppression", clear_on_submit=True):
    individu = st.multiselect("Salariés à supprimer", options=liste_nom)

    submitted = st.form_submit_button("Visualiser")
    
if submitted:
    dataset_id = dataset[dataset["identifiant"].isin(individu)]
    ids = dataset_id["id"].to_list()
    st.write(dataset_id)

# Utilisez un widget st.checkbox pour confirmer la suppression

confirmation_suppression = st.checkbox("Confirmer la suppression")

if confirmation_suppression and not dataset[dataset["identifiant"].isin(individu)]["id"].isin([1]).any():
    envoi_suppresion_donnee(dataset, individu)
if dataset[dataset["identifiant"].isin(individu)]["id"].isin([1]).any():
    st.write("On vas pas virer la directrice quand même !!")
    

footer()



