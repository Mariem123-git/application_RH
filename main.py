from config import setup_page, apply_custom_styles, MOT_DE_PASSE_ATTENDU

from auth import authentifier
from uploader import uploader_excel
import page_infos
import page_paie
import page_resultat
import page_indemnite
import page_fiscalite

import streamlit as st
import io
import pandas as pd
setup_page()
apply_custom_styles()

# — Vérification du mot de passe —
mot_de_passe = st.text_input("🔑 Entrez le mot de passe :", type="password")

if mot_de_passe != MOT_DE_PASSE_ATTENDU:
    st.error("⛔ Mot de passe incorrect")
    st.stop()

# — Application principale —
st.success("✅ Accès autorisé ! Bienvenue dans l'application RH sécurisée.")
authentifier()
xls, uploaded_file = uploader_excel()

# Sélection de la feuille
sheet_names = xls.sheet_names
selected_sheet = st.selectbox("👉 Sélectionner une feuille :", options=sheet_names)
df = xls.parse(selected_sheet)

with st.expander("📋 Voir les données brutes"):
    st.dataframe(df)

sheet_name = selected_sheet.strip().lower()



# === Redirection avec stockage des données complètes
if sheet_name == "informations générales":
    result = page_infos.run(df)

elif "paie" in sheet_name and "données" in sheet_name:
    result = page_paie.run(df, xls, uploaded_file)

elif sheet_name == "résultat final & paiement":
    result = page_resultat.run(df)

elif "indemnités" in sheet_name and "avantages" in sheet_name:
    result = page_indemnite.run(df)

elif "retenues" in sheet_name and "fiscalité" in sheet_name:
    result = page_fiscalite.run(df)

else:
    st.warning("Section non reconnue.")

