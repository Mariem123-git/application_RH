import streamlit as st

def authentifier():
    MOT_DE_PASSE_ATTENDU = "ADMIN2025"
    st.sidebar.title("🔑 Authentification")
    mot_de_passe = st.sidebar.text_input("Mot de passe :", type="password")

    if mot_de_passe != MOT_DE_PASSE_ATTENDU:
        st.sidebar.warning("⛔ Mot de passe incorrect.")
        st.stop()
    st.sidebar.success("✅ Accès autorisé.")
