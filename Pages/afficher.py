# Import des bibliothèques
import streamlit as st
from PIL import Image
import pandas as pd
from bibliotheque.lib import  *
from st_pages import Page, show_pages, add_page_title
from datetime import datetime 
from plotly.offline import iplot
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import sqlite3
from datetime import datetime

def reset():
    st.session_state["age"]=[17,99]
    st.session_state["genre"]=["M","F"]
    st.session_state["ville"]=liste_villes

# config de pages
config_site("wide")
formatage_de_la_page("style.css")
sidebar()
st.sidebar.markdown("<p class=titre_filtre>Filtres</p>", unsafe_allow_html=True)
ages = st.sidebar.slider("Tranche d'âges", min_value=17, max_value=99, value=(17,99), key="age" )
genre = st.sidebar.multiselect("Genres:",["F","M"],["F","M"], key="genre" )
liste_villes = récupérer_liste_ville()
villes = st.sidebar.multiselect("villes", liste_villes, liste_villes, key="ville")
reset = st.sidebar.button("reset", on_click=reset)



# titre, contexte et logos
header("Affichage des salariés","")


# Code principal
creation_base_et_table()

dataset = calcul_ages()

# filtre des âges
dataset["age"] = dataset["age"].astype(int)
dataset = dataset[dataset["age"] > ages[0]]
dataset = dataset[dataset["age"] < ages[1]]

# filtre des genres
dataset = dataset[dataset["genre"].isin(genre)]

# filtre des villes
dataset = dataset[dataset["nom_ville"].isin(villes)]
nombre_lignes = dataset["id"].count()
st.dataframe(dataset, hide_index=True, height= (nombre_lignes + 1) * 35 + 3, width=14000, column_config=dictionnaire_des_colonnes())

footer()