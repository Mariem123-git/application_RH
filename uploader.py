import streamlit as st
import pandas as pd

import streamlit as st
import pandas as pd

def uploader_excel():
    uploaded_file = st.sidebar.file_uploader(
        "Choisir fichier Excel",
        type=["xlsx"],
        key="file_upload_principal"  # <= Ajoute un `key` pour être sûr
    )
    if not uploaded_file:
        st.info("📁 Merci de téléverser un fichier Excel RH.")
        st.stop()
    return pd.ExcelFile(uploaded_file), uploaded_file


    # ✅ CHARGEMENT DES FEUILLES
    # ———————————————————————————
    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names

    selected_sheet = st.selectbox("👉 Sélectionner une feuille :", options=sheet_names)
    df = xls.parse(selected_sheet)

    # Affichage table brute
    with st.expander("📋 Voir les données brutes"):
        st.dataframe(df)

    sheet_name = selected_sheet.strip().lower()
