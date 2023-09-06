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

# config de pages
config_site("wide")
formatage_de_la_page("style.css")
sidebar()
st.sidebar.markdown("<p class=titre_filtre>Filtres</p>", unsafe_allow_html=True)
ages = st.sidebar.slider("Tranche d'âges", min_value=17, max_value=99, value=(17,99) )
genre = st.sidebar.multiselect("Genres:",["F","M"],["F","M"] )
liste_villes = récupérer_liste_ville()
villes = st.sidebar.multiselect("villes", liste_villes, liste_villes)

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

st.dataframe(dataset, hide_index=True, width=14000)

footer()