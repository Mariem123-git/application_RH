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
        df = df_filtered

    df = df.iloc[:-1, :]

    def detect_numeric_columns(df):
        """Détecte toutes les colonnes numériques dans le DataFrame"""
        numeric_cols = []

        # Colonnes à exclure de la détection automatique (colonnes non financières)
        excluded_cols = [
            'Noms & Prénoms', 'Matricule', 'N° CIN', 'N° CNSS', 'Code',
            'Nbre Jours', 'Heures suppl', 'Jours d\'absences', 'Section',
            'Date d\'embauche', 'Date de naissance', 'Situation familiale',
            'Nombre d\'enfants', 'Niveau d\'études', 'Fonction'
        ]

        for col in df.columns:
            if col not in excluded_cols:
                # Tenter de convertir en numérique
                try:
                    numeric_series = pd.to_numeric(df[col], errors='coerce')
                    # Vérifier s'il y a AU MOINS UNE valeur numérique valide
                    valid_count = numeric_series.notna().sum()

                    if valid_count > 0:  # Au moins une valeur numérique trouvée
                        positive_count = (numeric_series > 0).sum()

                        # Conditions d'inclusion très souples pour les données financières
                        if (positive_count == 0) or (positive_count / valid_count >= 0.05) or (valid_count <= 5):
                            numeric_cols.append(col)

                except:
                    continue

        return numeric_cols

    def afficher_statistiques_financieres(df):
        df_financier = df.copy()

        # ===== DÉTECTION AUTOMATIQUE DES COLONNES NUMÉRIQUES =====
        all_numeric_cols = detect_numeric_columns(df_financier)

        # Colonnes prédéfinies (pour maintenir la compatibilité)
        predefined_cols = [
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
                # Mettre à jour la liste des colonnes détectées
                if ancien_nom in all_numeric_cols:
                    all_numeric_cols.remove(ancien_nom)
                    all_numeric_cols.append(nouveau_nom)

        # Nouvelles colonnes détectées automatiquement
        new_cols = [col for col in all_numeric_cols if col not in predefined_cols]

        # Toutes les colonnes à traiter
        all_cols_to_process = predefined_cols + new_cols

        # Afficher les nouvelles colonnes détectées
        if new_cols:
            st.markdown("""
                <div style="background: linear-gradient(135deg, #00b894 0%, #00a085 100%); color: white; 
                     padding: 15px; border-radius: 10px; margin: 15px 0; font-weight: bold;">
                    ✅ Nouvelles colonnes financières détectées automatiquement
                </div>
                """, unsafe_allow_html=True)

            cols_info = []
            for col in new_cols:
                valid_count = pd.to_numeric(df_financier[col], errors='coerce').notna().sum()
                total_rows = len(df_financier)
                fill_percentage = (valid_count / total_rows) * 100
                cols_info.append(f"**{col}** ({valid_count}/{total_rows} entrées - {fill_percentage:.1f}%)")

            cols_text = ", ".join(cols_info)
            st.markdown(f"📊 {cols_text}")

        # Convertir toutes les colonnes numériques
        for col in all_cols_to_process:
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
        .stat-card {
            background: rgba(255,255,255,0.95);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-left: 5px solid #4CAF50;
            transition: transform 0.3s ease;
            margin: 10px 0;
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
        .new-col-card {
            background: rgba(255,255,255,0.95);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-left: 5px solid #a29bfe;
            transition: transform 0.3s ease;
            margin: 10px 0;
        }
        .new-col-card:hover {
            transform: translateY(-5px);
        }
        .new-col-value {
            font-size: 28px;
            font-weight: bold;
            color: #6c5ce7;
            margin: 10px 0;
        }
        </style>
        """, unsafe_allow_html=True)

        # Titre principal
        st.markdown('<div class="financial-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">ANALYSE FINANCIÈRE COMPLÈTE</div>', unsafe_allow_html=True)

        # Fonction pour calculer les statistiques
        def safe_sum(df, col):
            if col in df.columns:
                return pd.to_numeric(df[col], errors='coerce').sum()
            return 0

        def safe_mean(df, col):
            if col in df.columns:
                return pd.to_numeric(df[col], errors='coerce').mean()
            return 0

        # 1️⃣ STATISTIQUES DE BASE (TOTAUX) - Colonnes prédéfinies
        st.markdown('<div class="category-header"> STATISTIQUES DE BASE SUR LES MONTANTS</div>',
                    unsafe_allow_html=True)

        # Organiser les colonnes prédéfinies en groupes
        predefined_present = [col for col in predefined_cols if col in df_financier.columns]

        if predefined_present:
            # Diviser en chunks de 4 pour l'affichage
            chunks = [predefined_present[i:i + 4] for i in range(0, len(predefined_present), 4)]

            for chunk in chunks:
                cols = st.columns(len(chunk))

                for i, col in enumerate(chunk):
                    with cols[i]:
                        total = safe_sum(df_financier, col)
                        formatted_name = col.replace('_', ' ').title()
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-label">Total {formatted_name}</div>
                            <div class="stat-value">{total:,.2f} DH</div>
                        </div>
                        """, unsafe_allow_html=True)

        # 2️⃣ NOUVELLES COLONNES DÉTECTÉES AUTOMATIQUEMENT
        if new_cols:

            # Organiser les nouvelles colonnes en groupes de 3
            new_cols_chunks = [new_cols[i:i + 3] for i in range(0, len(new_cols), 3)]

            for chunk in new_cols_chunks:
                cols_new = st.columns(len(chunk))

                for i, col in enumerate(chunk):
                    with cols_new[i]:
                        total = safe_sum(df_financier, col)
                        formatted_name = col.replace('_', ' ').title()

                        # Informations sur le remplissage
                        valid_count = pd.to_numeric(df_financier[col], errors='coerce').notna().sum()
                        total_rows = len(df_financier)
                        fill_percentage = (valid_count / total_rows) * 100

                        st.markdown(f"""
                        <div class="new-col-card">
                            <div class="stat-label"> Total {formatted_name}</div>
                            <div class="new-col-value">{total:,.2f} DH</div>
                            <small style="color: #666; font-size: 0.8em;">
                            </small>
                        </div>
                        """, unsafe_allow_html=True)

        # 3️⃣ MOYENNES PAR SALARIÉ
        st.markdown('<div class="category-header">MOYENNES PAR SALARIÉ</div>', unsafe_allow_html=True)

        nb_salaries = len(df_financier)

        # Moyennes des colonnes prédéfinies
        if predefined_present:
            for chunk in chunks:
                cols = st.columns(len(chunk))

                for i, col in enumerate(chunk):
                    with cols[i]:
                        moyenne = safe_mean(df_financier, col)
                        formatted_name = col.replace('_', ' ').title()
                        st.markdown(f"""
                        <div class="stat-card" style="border-left-color: #FF9800;">
                            <div class="stat-label"> {formatted_name} Moyen</div>
                            <div class="stat-value" style="color: #FF9800;">{moyenne:,.2f} DH</div>
                        </div>
                        """, unsafe_allow_html=True)

        # Moyennes des nouvelles colonnes
        if new_cols:

            for chunk in new_cols_chunks:
                cols_new = st.columns(len(chunk))

                for i, col in enumerate(chunk):
                    with cols_new[i]:
                        moyenne = safe_mean(df_financier, col)
                        formatted_name = col.replace('_', ' ').title()

                        st.markdown(f"""
                        <div class="new-col-card" style="border-left-color: #fd79a8;">
                            <div class="stat-label"> {formatted_name} Moyen</div>
                            <div class="new-col-value" style="color: #fd79a8;">{moyenne:,.2f} DH</div>
                        </div>
                        """, unsafe_allow_html=True)

        # Taux de contribution si disponible
        if 'Taux de Contribution' in df_financier.columns:
            moy_taux = df_financier['Taux de Contribution'].mean()
            st.markdown(f"""
            <div class="stat-card" style="border-left-color: #FF9800; text-align: center;">
                <div class="stat-label">Taux de Contribution Moyen</div>
                <div class="stat-value" style="color: #FF9800;">{moy_taux:,.2f} %</div>
            </div>
            """, unsafe_allow_html=True)

        # 4️⃣ CALCULS GLOBAUX
        # Calculer les totaux de toutes les colonnes
        total_predefined = sum([safe_sum(df_financier, col) for col in predefined_present])
        total_new_cols = sum([safe_sum(df_financier, col) for col in new_cols])
        total_general = total_predefined + total_new_cols

        # Calculs spécifiques
        total_sbi = safe_sum(df_financier, 'SBI')
        total_mutuelle = safe_sum(df_financier, 'Retenue Mutuelle')
        total_cnss = safe_sum(df_financier, 'Retenue CNSS')
        total_cimr = safe_sum(df_financier, 'Retenue CIMR')
        charges_sociales = total_cnss + total_cimr + total_mutuelle

        # Résumé général
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, #4CAF50, #45a049); color: white; padding: 20px; 
             border-radius: 10px; margin: 20px 0; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            <h3>RÉSUMÉ GÉNÉRAL</h3>
            <p><strong>Nombre total de salariés analysés :</strong> {nb_salaries}</p>
            <p><strong>Masse salariale totale (SBI) :</strong> {total_sbi:,.2f} DH</p>
            <p><strong>Charges sociales totales :</strong> {charges_sociales:,.2f} DH</p>
            <p><strong>Total général (toutes colonnes) :</strong> {total_general:,.2f} DH</p>
            <p><strong>Nouvelles colonnes détectées :</strong> {len(new_cols)}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # 5️⃣ GÉNÉRATION DU RAPPORT EXCEL
        st.markdown('<div>', unsafe_allow_html=True)

        # Préparer les données pour le rapport
        resume_data = {
            "Indicateur": [],
            "Valeur": []
        }

        # Ajouter les colonnes prédéfinies
        for col in predefined_present:
            formatted_name = f"Total {col.replace('_', ' ').title()}"
            resume_data["Indicateur"].append(formatted_name)
            resume_data["Valeur"].append(safe_sum(df_financier, col))

        # Ajouter les nouvelles colonnes
        for col in new_cols:
            formatted_name = f"Total {col.replace('_', ' ').title()}"
            resume_data["Indicateur"].append(formatted_name)
            resume_data["Valeur"].append(safe_sum(df_financier, col))

        # Ajouter les totaux généraux
        resume_data["Indicateur"].extend([
            "Charges sociales totales",
            "Nombre de salariés"
        ])
        resume_data["Valeur"].extend([
            charges_sociales,
            nb_salaries
        ])

        df_resume = pd.DataFrame(resume_data)

        # Préparer les données de détail des nouvelles colonnes
        new_cols_detail = []
        if new_cols:
            for col in new_cols:
                valid_count = pd.to_numeric(df_financier[col], errors='coerce').notna().sum()
                total_rows = len(df_financier)
                fill_percentage = (valid_count / total_rows) * 100
                moyenne = safe_mean(df_financier, col)

                new_cols_detail.append({
                    'Nouvelle Colonne': col,
                    'Total': f"{safe_sum(df_financier, col):,.2f} DH",
                    'Moyenne': f"{moyenne:,.2f} DH",
                    'Entrées valides': valid_count,
                    'Total lignes': total_rows,
                    'Pourcentage remplissage': f"{fill_percentage:.1f}%",
                    'Statut': (
                        "Optimal (80%+)" if fill_percentage >= 80 else
                        "Bon (50-79%)" if fill_percentage >= 50 else
                        "Acceptable (20-49%)" if fill_percentage >= 20 else
                        "Attention (<20%)" if fill_percentage > 0 else
                        "Vide (0%)"
                    )
                })

        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            # Feuille principale avec résumé
            df_resume.to_excel(writer, index=False, sheet_name='Résumé Financier')

            # Feuille avec données brutes
            df_financier.to_excel(writer, index=False, sheet_name='Données Complètes')

            # Feuille avec détail des nouvelles colonnes si présentes
            if new_cols_detail:
                df_new_detail = pd.DataFrame(new_cols_detail)
                df_new_detail.to_excel(writer, index=False, sheet_name='Nouvelles Colonnes')

        excel_buffer.seek(0)

        # Message de résumé
        if new_cols:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #00b894 0%, #00a085 100%); color: white; 
                     padding: 15px; border-radius: 10px; margin: 15px 0; font-weight: bold;">
                    <strong>Rapport généré avec succès!</strong><br>
                    {len(new_cols)} nouvelle(s) colonne(s) financière(s) détectée(s) et intégrée(s)<br>
                    
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%); color: white; 
                     padding: 15px; border-radius: 10px; margin: 15px 0; font-weight: bold;">
                    📋 <strong>Rapport généré avec les colonnes standards</strong><br>
                    ℹ️ Aucune nouvelle colonne financière détectée
                </div>
                """, unsafe_allow_html=True)

        st.download_button(
            label="📥 Télécharger le résumé financier complet",
            data=excel_buffer,
            file_name="resume_financier_automatique.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Le rapport inclut toutes les colonnes financières détectées automatiquement"
        )



        return df_resume, new_cols

    # Utilisation du code
    try:
        # Détecter si on a des colonnes financières
        financial_indicators = [
            'Retenue Mutuelle', 'Retenues Mutuelles', 'Retenues Mut',
            'SBI', 'Salaire Brut Imposable',
            'IGR', 'CNSS', 'CIMR',
            'Retenue', 'Frais'
        ]

        has_financial_data = any(
            any(indicator.lower() in col.lower() for indicator in financial_indicators)
            for col in df.columns
        )

        if has_financial_data:
            df_resume, new_cols = afficher_statistiques_financieres(df)
        else:
            st.warning(
                "⚠️ Aucune donnée financière détectée. Le système recherche des colonnes contenant: "
                "Retenue, SBI, IGR, CNSS, CIMR, Frais, etc.")

    except Exception as e:
        st.error(f"❌ Erreur lors du traitement des données financières : {str(e)}")
