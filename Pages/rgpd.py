# Import des bibliothèques
import streamlit as st
from PIL import Image
import pandas as pd
from bibliotheque.lib import  *
from st_pages import Page, show_pages, add_page_title

config_site("centered")
sidebar()

# titre, contexte et logos
header("RGPD de PaddlePersonnel","")


explication = """
            Les données stockées dans cette application sont uniquement des données fictives, à des fins de démonstrations et de formations.\n
            Les données sont stockés sur une base de données pour les afficher, les modifier, ou les supprimer.\n
            L'utilisateur consent à ces traitements, et s'engage à enregistrer uniquement des données fictives.\n
            """
st.write(explication)

rgpd = """

**Déclaration de Conformité au RGPD** \n
Cette déclaration de conformité au Règlement Général sur la Protection des Données (RGPD) concerne l'application de gestion de personnel fictive nommée PaddlePersonnel. Cette application a été conçue dans un but pédagogique et n'utilise que des données fictives. Nous prenons la protection des données personnelles très au sérieux et nous nous engageons à respecter les principes et les obligations du RGPD.

**1. Collecte de Données** \n
L'application PaddlePersonnel collecte uniquement des données personnelles fictives dans le but de fournir des fonctionnalités de gestion de personnel. Ces données comprennent, mais ne se limitent pas à : noms, prénoms, adresses e-mail, dates de naissance, genres, dates d'entrée dans l'entreprise, et autres informations de contact. Aucune donnée personnelle réelle n'est collectée ni stockée.

**2. Utilisation des Données** \n 
Les données collectées dans l'application PaddlePersonnel sont utilisées exclusivement à des fins pédagogiques. Elles ne sont pas partagées, vendues ou divulguées à des tiers, car il s'agit de données fictives. Les utilisateurs de l'application ont la possibilité de consulter, modifier et supprimer ces données.

**3. Sécurité des Données** \n   
Nous prenons des mesures de sécurité appropriées pour protéger les données fictives stockées dans l'application PaddlePersonnel. Cela inclut la mise en œuvre de pratiques de sécurité pour empêcher tout accès non autorisé aux données.

**4. Droits des Utilisateurs** \n   
Les utilisateurs de l'application PaddlePersonnel n'ont pas de droits spécifiques en vertu du RGPD, car aucune donnée personnelle réelle n'est traitée. Cependant, ils ont le droit de consulter, modifier et supprimer les données fictives.

**5. Contact** \n   
Si vous avez des questions ou des préoccupations concernant la manière dont vos données fictives sont traitées dans l'application PaddlePersonnel, vous pouvez nous contacter à l'adresse mail suivante : melo.surseine@gmail.com.

**6. Modifications de la Politique** \n   
Nous nous réservons le droit de mettre à jour cette déclaration de conformité au RGPD à tout moment. Toutes les modifications seront publiées sur cette page.

"""
st.markdown(rgpd)

footer()