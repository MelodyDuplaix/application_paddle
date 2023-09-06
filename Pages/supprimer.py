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

with st.form("suppression", clear_on_submit=True):
    individu = st.multiselect("Salariés à supprimer", options=liste_nom)

    submitted = st.form_submit_button("Visualiser")
    
if submitted:
    dataset_id = dataset[dataset["identifiant"].isin(individu)]
    ids = dataset_id["id"].to_list()
    st.write(dataset_id)

# Utilisez un widget st.checkbox pour confirmer la suppression
confirmation_suppression = st.checkbox("Confirmer la suppression")

if confirmation_suppression:
    dataset_id = dataset[dataset["identifiant"].isin(individu)]
    ids = dataset_id["id"].to_list()
    connexion = sqlite3.connect("data/personnel_societe_paddle")
    cursor = connexion.cursor()
    for id in ids:
        try:
            cursor.execute(f"DELETE FROM salaries WHERE id_salarie = '{id}';")
        except sqlite3.IntegrityError as e:
            st.write(e)
    connexion.commit()
    connexion.close()
    st.write("Les données ont bien été supprimées")


footer()



