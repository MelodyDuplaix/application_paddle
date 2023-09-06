# Import des bibliothèques
import streamlit as st
from PIL import Image
import pandas as pd
from bibliotheque.lib import  *
from st_pages import Page, show_pages, add_page_title
import numpy as np
import sqlite3
import datetime

config_site("centered")
sidebar()


# titre, contexte et logos
header("Tableau de modification des salariés","")




# Code principal

# Récupération des salariés
dataset = récupération_dataset_total()
dataset["identifiant"] = dataset["prenom"] + " " + dataset["nom_sa"]
liste_nom = dataset["identifiant"].to_list()

individu = st.selectbox("Salariés à modifier", options=liste_nom)


ligne_individu = dataset[dataset["identifiant"] == individu]
id = ligne_individu["id"]
with st.form("Formulaire d'ajout", clear_on_submit=False):
    prenom = st.text_area("Prénom", max_chars=25, placeholder="Pas de prénom", height=1, key="prenom", value=ligne_individu["prenom"].values[0])

    nom = st.text_area("Nom", max_chars=25, placeholder="Pas de nom", height=1, key="nom", value=ligne_individu["nom_sa"].values[0])

    mail = st.text_area("Mail", max_chars=50, placeholder="Pas de mail", height=1, key="mail", value=ligne_individu["mail"].values[0])
    if mail and( not "@" in mail or " " in mail):
        st.write(":red[Le mail n'est pas valide !]")

    today = datetime.datetime.now()
    date_de_naissance= date_obj = datetime.datetime.strptime(ligne_individu["date_naissance"].values[0], "%Y-%m-%d")
    date_de_naissance = st.date_input(
        "Date de naissance", max_value=datetime.date((today.year-18), 1, 1), min_value= datetime.date((today.year-100), 1, 1),
        format="YYYY.MM.DD", key="date_naissance", value=date_de_naissance
    )
    if ligne_individu["genre"].values[0] == "F":
        genres_possible = ("F","M")
    else:
        genres_possible = ("M","F")

    genre = st.selectbox("Genre", genres_possible, help="Homme : H Femme : F", key="genre")

    date_entree= date_obj = datetime.datetime.strptime(ligne_individu["date_arrivee"].values[0], "%Y-%m-%d")
    date_arrive = st.date_input(
        "Date d'entrée dans l'entreprise", min_value= datetime.date((today.year-60), 1, 1),
        format="YYYY.MM.DD", key="date_arrive", value=date_entree
    )
    
    liste_ville = récupérer_liste_ville()
    liste_ville_update = liste_ville.copy()
    liste_ville_update.remove(ligne_individu["nom_ville"].values[0])
    liste_ville_update.insert(0, ligne_individu["nom_ville"].values[0])
    localisation = st.selectbox("Ville",liste_ville_update, key="localisation")
    table_ville = récupérer_tableau_ville()
    localisation_id = table_ville[table_ville["nom"]==localisation]["id"].values

    date_sortie = st.date_input("Date de sortie", format="YYYY.MM.DD", value=datetime.date((today.year+100), 1, 1), min_value= datetime.date((today.year-60), 1, 1), help="Veuillez laissez la date  " + datetime.date((today.year+100), 1, 1).strftime("%Y-%m-%d") + "  si la date est nulle")
    if date_sortie == datetime.date((today.year+100), 1, 1):
        date_sortie = ""
    else:
        date_sortie = date_sortie.strftime("%Y-%m-%d")
    
    envoie = st.form_submit_button("Envoyer")
    if envoie:
        connexion = sqlite3.connect("data/personnel_societe_paddle")
        cursor = connexion.cursor()
        date_de_naissance_str = date_de_naissance.strftime("%Y-%m-%d")
        date_arrive_str = date_arrive.strftime("%Y-%m-%d")
        reponse = [prenom.capitalize(), nom.upper(), mail, genre, date_de_naissance_str, date_arrive_str, int(localisation_id), date_sortie,  int(id)]
        # Exécutez la commande SQL UPDATE pour mettre à jour la ligne
        try:
            cursor.execute(""" UPDATE salaries
            SET prenom = ?, nom_sa = ?, mail = ?, genre = ?, date_naissance = ?, date_arrivee = ?, id_ville = ?, date_sortie = ?
            WHERE id_salarie = ?;
        """, reponse)
        except sqlite3.IntegrityError as e:
            st.write(e)
        connexion.commit()
        connexion.close()
        st.write("Les données ont bien été mises à jour")


footer()