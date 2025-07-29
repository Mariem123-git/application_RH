import pandas as pd
import streamlit as st
import unicodedata

def recherche_employe(df):
    st.markdown("---")
    st.subheader("🔍 Recherche d'Employé")

    # ➜ Cas 1 : colonne combinée "Nom&Prénom"
    full_name_cols = [col for col in df.columns if 'nom' in col.lower() and 'prenom' in col.lower()]

    if full_name_cols:
        full_name_col = full_name_cols[0]
        search_full_name = st.text_input("Nom & Prénom", placeholder="Tapez une partie du nom ou prénom...")
        search_button = st.button(" Rechercher", type="primary")

        if search_full_name or search_button:
            filtered_df = df[df[full_name_col].str.contains(search_full_name, case=False, na=False)]

            if not filtered_df.empty:
                st.success(f"✅ {len(filtered_df)} employé(s) trouvé(s)")
                st.dataframe(filtered_df, use_container_width=True)
            else:
                st.warning("❌ Aucun employé trouvé avec ces critères")

        st.markdown("---")
        return filtered_df if 'filtered_df' in locals() else df

    # ➜ Cas 2 : colonnes séparées Nom et Prénom
    else:
        nom_cols = [col for col in df.columns if 'nom' in col.lower()]
        prenom_cols = [col for col in df.columns if 'prenom' in col.lower() or 'prénom' in col.lower()]

        if nom_cols and prenom_cols:
            nom_col = nom_cols[0]
            prenom_col = prenom_cols[0]

            search_nom = st.text_input("Nom", placeholder="Tapez le nom...")
            search_prenom = st.text_input("Prénom", placeholder="Tapez le prénom...")
            search_button = st.button("🔍 Rechercher", key="search_nom_prenom")

            if search_nom or search_prenom or search_button:
                filtered_df = df.copy()

                if search_nom:
                    filtered_df = filtered_df[filtered_df[nom_col].str.contains(search_nom, case=False, na=False)]
                if search_prenom:
                    filtered_df = filtered_df[filtered_df[prenom_col].str.contains(search_prenom, case=False, na=False)]

                if not filtered_df.empty:
                    st.success(f"✅ {len(filtered_df)} employé(s) trouvé(s)")
                    st.dataframe(filtered_df, use_container_width=True)
                else:
                    st.warning("❌ Aucun employé trouvé avec ces critères")

            st.markdown("---")
            return filtered_df if 'filtered_df' in locals() else df

        else:
            st.warning("❗ Colonne Nom ou Prénom non trouvée")
            st.markdown("---")
            return df