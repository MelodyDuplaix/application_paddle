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
header("Formulaire d'ajout d'un salarié","")


# Code principal

st.info(body="Tous les champs sont obligatoires.", icon="❗")

# Formulaire
with st.form("Formulaire d'ajout", clear_on_submit=True):
    prenom = st.text_area("Prénom", max_chars=25, placeholder="Pas de prénom", height=1, key="prenom")
    nom = st.text_area("Nom", max_chars=25, placeholder="Pas de nom", height=1, key="nom")
    mail = st.text_area("Mail", max_chars=50, placeholder="Pas de mail", height=1, key="mail")
    if mail and( not "@" in mail or " " in mail):
        st.write(":red[Le mail n'est pas valide !]")
    today = datetime.datetime.now()
    date_de_naissance = st.date_input(
        "Date de naissance", max_value=datetime.date((today.year-18), 1, 1), min_value= datetime.date((today.year-100), 1, 1),
        format="YYYY.MM.DD", value= datetime.date((today.year-30), 1, 1), key="date_naissance"
    )
    genre = st.selectbox("Genre", ("F","M"), help="Homme : H Femme : F", key="genre")
    date_arrive = st.date_input(
        "Date d'entrée dans l'entreprise", min_value= datetime.date((today.year-60), 1, 1),
        format="YYYY.MM.DD", key="date_arrive"
    )
    liste_ville = récupérer_liste_ville()
    localisation = st.selectbox("Ville",liste_ville, key="localisation")
    
    
    submitted = st.form_submit_button("Envoyer")
    if submitted and prenom and nom and mail:
        connexion = sqlite3.connect("data/personnel_societe_paddle")
        cursor = connexion.cursor()
        id_ville = liste_ville.index(localisation)+1
        date_naissance = datetime.datetime.strptime(str(date_de_naissance),"%Y-%m-%d")
        reponse = [prenom.capitalize(), nom.upper(), mail, genre, date_de_naissance, date_arrive, id_ville]
        try : 
            cursor.execute("INSERT INTO salaries('prenom','nom_sa', 'mail', 'genre', 'date_naissance', 'date_arrivee', 'id_ville') VALUES(?,?,?,?,?,?,?)", reponse)
        except sqlite3.IntegrityError as e:
            st.write(e)
        connexion.commit()
        connexion.close()
        st.write("Les données ont bien été envoyé")



    
    
footer()