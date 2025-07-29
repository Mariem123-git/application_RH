import streamlit as st
import pandas as pd
import numpy as np
from utils import recherche_employe

def run(df):

    import io


    df_filtered = recherche_employe(df)
    # Option : utiliser le DataFrame filtré ou non
    use_filtered = st.checkbox("📊 Utiliser le filtre pour les graphiques", value=False)
    if use_filtered:
        df = df_filtered  # ✅ Pas de deux-points ici !

    df = df.iloc[:-1, :]


    def afficher_statistiques_financieres(df):
        df_financier = df.copy()

        # Vérifier que les colonnes nécessaires existent
        colonnes_requises = [
            'Retenue Mutuelle', 'Retenue CNSS', 'Retenue CIMR',
            'SBI', 'Frais Professionnels', 'IGR Brut', 'IGR Net'
        ]

        # Adapter les noms de colonnes si différents
        colonnes_mapping = {
            'Retenues Mut': 'Retenue Mutuelle',
            'Retenues CNSS': 'Retenue CNSS',
            'Retenues CIMR': 'Retenue CIMR',
            'Salaire Brut Imposable': 'SBI',
            'IGR_Brut': 'IGR Brut',
            'IGR_Net': 'IGR Net',
            'Frais professionnels': 'Frais Professionnels'
        }

        # Renommer les colonnes si nécessaire
        for ancien_nom, nouveau_nom in colonnes_mapping.items():
            if ancien_nom in df_financier.columns:
                df_financier = df_financier.rename(columns={ancien_nom: nouveau_nom})

        # Convertir en numérique et nettoyer les données
        for col in colonnes_requises:
            if col in df_financier.columns:
                df_financier[col] = pd.to_numeric(df_financier[col], errors='coerce').fillna(0)

        # Calculer le taux de contribution si pas présent
        if 'Taux de Contribution' not in df_financier.columns:
            if 'SBI' in df_financier.columns and 'IGR Net' in df_financier.columns:
                df_financier['Taux de Contribution'] = np.where(
                    df_financier['SBI'] > 0,
                    (df_financier['IGR Net'] / df_financier['SBI']) * 100,
                    0
                )

        # CSS pour le style
        st.markdown("""
        <style>
        .financial-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        .section-title {
            color: white;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 25px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .stat-card {
            background: rgba(255,255,255,0.95);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-left: 5px solid #4CAF50;
            transition: transform 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-5px);
        }
        .stat-value {
            font-size: 28px;
            font-weight: bold;
            color: #2E7D32;
            margin: 10px 0;
        }
        .stat-label {
            font-size: 14px;
            color: #666;
            font-weight: 500;
        }
        .category-header {
            background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
            color: white;
            padding: 15px;
            border-radius: 10px;
            font-weight: bold;
            font-size: 18px;
            margin: 20px 0 15px 0;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        </style>
        """, unsafe_allow_html=True)

        # Titre principal
        st.markdown('<div class="financial-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-title"> ANALYSE FINANCIÈRE COMPLÈTE </div>', unsafe_allow_html=True)

        # 1️⃣ STATISTIQUES DE BASE (TOTAUX)
        st.markdown('<div class="category-header"> STATISTIQUES DE BASE SUR LES MONTANTS</div>',
                    unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if 'Retenue Mutuelle' in df_financier.columns:
                total_mutuelle = df_financier['Retenue Mutuelle'].sum()
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label"> Total Retenues Mutuelles</div>
                    <div class="stat-value">{total_mutuelle:,.2f} DH</div>
                </div>
                """, unsafe_allow_html=True)

            if 'SBI' in df_financier.columns:
                total_sbi = df_financier['SBI'].sum()
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label"> Total Salaire Brut Imposable</div>
                    <div class="stat-value">{total_sbi:,.2f} DH</div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            if 'Retenue CNSS' in df_financier.columns:
                total_cnss = df_financier['Retenue CNSS'].sum()
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Total Retenues CNSS</div>
                    <div class="stat-value">{total_cnss:,.2f} DH</div>
                </div>
                """, unsafe_allow_html=True)

            if 'Frais Professionnels' in df_financier.columns:
                total_frais = df_financier['Frais Professionnels'].sum()
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label"> Total Frais Professionnels</div>
                    <div class="stat-value">{total_frais:,.2f} DH</div>
                </div>
                """, unsafe_allow_html=True)

        with col3:
            if 'Retenue CIMR' in df_financier.columns:
                total_cimr = df_financier['Retenue CIMR'].sum()
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label"> Total Retenues CIMR</div>
                    <div class="stat-value">{total_cimr:,.2f} DH</div>
                </div>
                """, unsafe_allow_html=True)

            if 'IGR Brut' in df_financier.columns:
                total_igr_brut = df_financier['IGR Brut'].sum()
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Total IGR Brut</div>
                    <div class="stat-value">{total_igr_brut:,.2f} DH</div>
                </div>
                """, unsafe_allow_html=True)

        with col4:
            if 'IGR Net' in df_financier.columns:
                total_igr_net = df_financier['IGR Net'].sum()
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label"> Total IGR Net</div>
                    <div class="stat-value">{total_igr_net:,.2f} DH</div>
                </div>
                """, unsafe_allow_html=True)

        # 2️⃣ MOYENNES PAR SALARIÉ
        st.markdown('<div class="category-header"> MOYENNES PAR SALARIÉ</div>', unsafe_allow_html=True)

        nb_salaries = len(df_financier)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if 'Retenue Mutuelle' in df_financier.columns:
                moy_mutuelle = df_financier['Retenue Mutuelle'].mean()
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #FF9800;">
                    <div class="stat-label"> Retenue Mutuelle Moyenne</div>
                    <div class="stat-value" style="color: #FF9800;">{moy_mutuelle:,.2f} DH</div>
                </div>
                """, unsafe_allow_html=True)

            if 'SBI' in df_financier.columns:
                moy_sbi = df_financier['SBI'].mean()
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #FF9800;">
                    <div class="stat-label"> SBI Moyen</div>
                    <div class="stat-value" style="color: #FF9800;">{moy_sbi:,.2f} DH</div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            if 'Retenue CNSS' in df_financier.columns:
                moy_cnss = df_financier['Retenue CNSS'].mean()
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #FF9800;">
                    <div class="stat-label"> Retenue CNSS Moyenne</div>
                    <div class="stat-value" style="color: #FF9800;">{moy_cnss:,.2f} DH</div>
                </div>
                """, unsafe_allow_html=True)

            if 'IGR Brut' in df_financier.columns:
                moy_igr_brut = df_financier['IGR Brut'].mean()
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #FF9800;">
                    <div class="stat-label">IGR Brut Moyen</div>
                    <div class="stat-value" style="color: #FF9800;">{moy_igr_brut:,.2f} DH</div>
                </div>
                """, unsafe_allow_html=True)

        with col3:
            if 'Retenue CIMR' in df_financier.columns:
                moy_cimr = df_financier['Retenue CIMR'].mean()
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #FF9800;">
                    <div class="stat-label"> Retenue CIMR Moyenne</div>
                    <div class="stat-value" style="color: #FF9800;">{moy_cimr:,.2f} DH</div>
                </div>
                """, unsafe_allow_html=True)

            if 'IGR Net' in df_financier.columns:
                moy_igr_net = df_financier['IGR Net'].mean()
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #FF9800;">
                    <div class="stat-label"> IGR Net Moyen</div>
                    <div class="stat-value" style="color: #FF9800;">{moy_igr_net:,.2f} DH</div>
                </div>
                """, unsafe_allow_html=True)

        with col4:
            if 'Frais Professionnels' in df_financier.columns:
                moy_frais = df_financier['Frais Professionnels'].mean()
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #FF9800;">
                    <div class="stat-label"> Frais Professionnels Moyens</div>
                    <div class="stat-value" style="color: #FF9800;">{moy_frais:,.2f} DH</div>
                </div>
                """, unsafe_allow_html=True)

            if 'Taux de Contribution' in df_financier.columns:
                moy_taux = df_financier['Taux de Contribution'].mean()
                st.markdown(f"""
                <div class="stat-card" style="border-left-color: #FF9800;">
                    <div class="stat-label"> Taux de Contribution Moyen</div>
                    <div class="stat-value" style="color: #FF9800;">{moy_taux:,.2f} %</div>
                </div>
                """, unsafe_allow_html=True)

        # Résumé général
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #4CAF50, #45a049); color: white; padding: 20px; 
             border-radius: 10px; margin: 20px 0; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            <h3>RÉSUMÉ GÉNÉRAL</h3>
            <p><strong>Nombre total de salariés analysés :</strong> {nb_salaries}</p>
            <p><strong>Masse salariale totale (SBI) :</strong> {total_sbi:,.2f} DH</p>
            <p><strong>Charges sociales totales :</strong> {(total_cnss + total_cimr + total_mutuelle):,.2f} DH</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        import io
        st.markdown('<div>', unsafe_allow_html=True)

        resume_data = {
            "Indicateur": [
                "Total Retenue Mutuelle",
                "Total Retenue CNSS",
                "Total Retenue CIMR",
                "Total SBI",
                "Total Frais Professionnels",
                "Total IGR Brut",
                "Total IGR Net",
                "Charges sociales totales"
            ],
            "Valeur": [
                total_mutuelle,
                total_cnss,
                total_cimr,
                total_sbi,
                total_frais,
                total_igr_brut,
                total_igr_net,
                total_cnss + total_cimr + total_mutuelle
            ]
        }
        df_resume = pd.DataFrame(resume_data)

        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df_resume.to_excel(writer, index=False, sheet_name='Résumé Financier')
        excel_buffer.seek(0)

        st.download_button(
            label="Télécharger le résumé financier",
            data=excel_buffer,
            file_name="resume_financier.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


    # Utilisation du code
    # Si les données financières sont dans une feuille séparée :
    try:
        # Exemple pour lire une feuille spécifique
        # df_financier = pd.read_excel("votre_fichier.xlsx", sheet_name="Feuille_Financiere")

        # Ou si c'est déjà dans df sous certaines colonnes
        if any(col in df.columns for col in
               ['Retenue Mutuelle', 'Retenues Mutuelles', 'SBI', 'Salaire Brut Imposable']):
            afficher_statistiques_financieres(df)
        else:
            st.warning(
                "⚠️ Les données financières ne sont pas trouvées. Vérifiez le nom de la feuille ou les colonnes.")


    except Exception as e:
        st.error(f" Erreur lors du chargement des données financières : {str(e)}")

