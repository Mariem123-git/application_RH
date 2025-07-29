# ——————————————————————————————————————————————
# ✅ CONFIGURATION
# ——————————————————————————————————————————————

import streamlit as st

# Configuration de la page Streamlit
def setup_page():
    st.set_page_config(
        page_title="🔐 Application RH Sécurisée",
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# Styles CSS personnalisés
def apply_custom_styles():
    """Applique les styles CSS personnalisés à l'application"""
    st.markdown("""
        <style>
        .main {background-color: #f7f9fb;}
        h1, h2, h3 {color: #003366;}
        div.stButton > button {background-color: #003366; color: white;}
        div.stTextInput > div > input {background-color: #f0f5f9;}
        .stDataFrame {border: 1px solid #003366;}
        </style>
    """, unsafe_allow_html=True)

# Récupération du mot de passe depuis les secrets
MOT_DE_PASSE_ATTENDU = st.secrets["general"]["password"]

