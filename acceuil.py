# Import des bibliothèques
import streamlit as st
import pandas as pd
from bibliotheque.lib import  *
from st_pages import Page, show_pages, add_page_title

config_site("centered")
sidebar()
header_avec_image("Récapitulatif des salariés", "")




# Code principal

creation_base_et_table()

# Compte du nombre total
nombre_total = calcul_total()


# Calcul des âges
dataset_age = groupement_ages()
graph_tranche_age = graph_age(dataset_age)


# Groupement par genres
dataset_genre = calcul_genres()
graph_genre = graph_genres(dataset_genre)

# Groupement par villes
dataset_ville = calcul_villes()
graph_ville = graph_villes(dataset_ville)

# Affichage
colonne1_1, colonne2_1 = st.columns(2)
with colonne1_1:
    st.write("Nombre de salariés")
    st.write(nombre_total[0])
with colonne2_1:
    st.write("Répartition hommes/femmes")
    st.plotly_chart(graph_genre, use_container_width=True)
    
colonne1_2, colonne2_2 = st.columns(2)
with colonne1_2:
    st.write("Répartition par âges")
    st.plotly_chart(graph_tranche_age, use_container_width=True)
with colonne2_2:
    st.write("Répartition par villes")
    st.plotly_chart(graph_ville, use_container_width=True)
    
footer()