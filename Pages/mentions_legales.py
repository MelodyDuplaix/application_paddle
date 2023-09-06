# Import des bibliothèques
import streamlit as st
from PIL import Image
import pandas as pd
from bibliotheque.lib import  *
from st_pages import Page, show_pages, add_page_title

config_site("centered")
sidebar()

# titre, contexte et logos
header("Mentions Légales","")

explication = """
**Mentions légales**\n

**Éditeur du site :**\n
PaddlePersonnel\n
Adresse : CEFIM\n
Téléphone : +XX (0)XX XX XX XX\n
E-mail : contact@paddlepersonnel.com

**Directeur de la publication :**\n
Lyly LALICORNE\n
Adresse e-mail : llico@arcenciel.com

**Hébergement :**\n
Nom de l'hébergeur fictif\n
Adresse de l'hébergeur fictif\n
Téléphone : +XX (0)XX XX XX XX\n
E-mail : support@hebergeurfictif.com

**Propriété intellectuelle :**\n
L'ensemble du contenu de ce site, incluant mais sans s'y limiter, les textes, les images, les vidéos, les logos et les éléments graphiques, est la propriété de PaddlePersonnel et est protégé par les lois sur la propriété intellectuelle. Toute reproduction, distribution ou utilisation non autorisée de ce contenu est strictement interdite.

**Protection des données personnelles :**\n
Nous recueillons des données personnelles à des fins de gestion de personnel fictives. Ces données sont traitées conformément aux réglementations en vigueur et ne sont pas utilisées à des fins commerciales. Vous avez le droit d'accéder, de rectifier ou de supprimer vos données personnelles en nous contactant à l'adresse e-mail : donnees@paddlepersonnel.com.

**Cookies :**\n
Ce site utilise des cookies pour améliorer l'expérience de l'utilisateur. En naviguant sur ce site, vous acceptez l'utilisation de cookies conformément à notre politique de cookies. Vous pouvez modifier vos préférences de cookies dans les paramètres de votre navigateur.

**Responsabilité :**\n
Nous nous efforçons de maintenir les informations de ce site à jour, mais nous ne pouvons garantir l'exactitude, l'exhaustivité ou la pertinence des informations fournies. Nous déclinons toute responsabilité pour les dommages directs ou indirects résultant de l'utilisation de ce site.

**Liens externes :**\n
Ce site peut contenir des liens vers des sites web tiers. Nous déclinons toute responsabilité pour le contenu de ces sites et ne pouvons garantir leur sécurité ou leur conformité aux réglementations en vigueur.

"""

st.markdown(explication)

footer()