from utils import recherche_employe
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from uploader import uploader_excel


def run(df, xls, uploaded_file):
    import streamlit as st

    df_filtered = recherche_employe(df)

    # Option : utiliser le DataFrame filtré ou non
    use_filtered = st.checkbox("📊 Utiliser le filtre pour les graphiques", value=False)
    if use_filtered:
        df = df_filtered

    # CSS personnalisé pour styliser la section paie
    st.markdown("""
        <style>
            /* Cartes métriques pour la paie */
            .paie-metric-card {
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                text-align: center;
                margin: 10px;
                border: 1px solid rgba(255,255,255,0.2);
                backdrop-filter: blur(10px);
            }

            .paie-metric-card h3 {
                color: white;
                margin-bottom: 10px;
                font-size: 1.1em;
                font-weight: bold;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }

            .paie-metric-card p {
                color: #f0f0f0;
                font-size: 1.8em;
                margin: 0;
                font-weight: bold;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }

            /* Cartes spécifiques pour la paie */
            .card-hs {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }

            .card-rendement {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            }

            .card-anciennete-prime {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            }

            .card-poste {
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            }

            .card-total-primes {
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            }

            .card-custom {
                background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%);
            }

            /* Section header pour la paie */
            .paie-section-header {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 15px;
                margin: 25px 0;
                text-align: center;
                box-shadow: 0 6px 20px rgba(0,0,0,0.2);
                border: 2px solid rgba(255,255,255,0.1);
            }

            .paie-section-header h2 {
                margin: 0;
                font-size: 1.8em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }

            /* Graphiques avec fond coloré */
            .chart-container {
                background: rgba(255,255,255,0.9);
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 6px 20px rgba(0,0,0,0.1);
                margin: 20px 0;
            }

            /* Alertes stylisées */
            .custom-warning {
                background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
                color: #2d3436;
                padding: 15px;
                border-radius: 10px;
                border-left: 5px solid #e17055;
                margin: 15px 0;
                font-weight: bold;
            }

            .custom-info {
                background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
                color: white;
                padding: 15px;
                border-radius: 10px;
                border-left: 5px solid #0984e3;
                margin: 15px 0;
                font-weight: bold;
            }

            .custom-error {
                background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
                color: white;
                padding: 15px;
                border-radius: 10px;
                border-left: 5px solid #e84393;
                margin: 15px 0;
                font-weight: bold;
            }

            .custom-success {
                background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
                color: white;
                padding: 15px;
                border-radius: 10px;
                border-left: 5px solid #00a085;
                margin: 15px 0;
                font-weight: bold;
            }
        </style>
        """, unsafe_allow_html=True)

    import streamlit as st
    def process_paie_data(df, uploaded_file=None):
        absences_Section = None

        # Header principal
        st.markdown('<div class="paie-section-header"><h2> Statistiques Paie</h2></div>', unsafe_allow_html=True)

        # Nettoyer : supprimer la dernière ligne souvent vide
        df = df.iloc[:-1, :]

        # ===== NOUVELLE FONCTIONNALITÉ : DÉTECTION AUTOMATIQUE =====
        def detect_numeric_columns(df):
            """Détecte toutes les colonnes numériques dans le DataFrame"""
            numeric_cols = []

            # Colonnes à exclure de la détection automatique (colonnes non monétaires)
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
                        # Vérifier s'il y a AU MOINS UNE valeur numérique valide (même si la colonne est partiellement vide)
                        valid_count = numeric_series.notna().sum()

                        if valid_count > 0:  # Au moins une valeur numérique trouvée
                            # Si toutes les valeurs valides sont 0, on l'inclut quand même
                            # Si il y a des valeurs > 0, on vérifie le ratio (plus souple)
                            positive_count = (numeric_series > 0).sum()

                            # Conditions d'inclusion plus souples :
                            # 1. Si toutes les valeurs sont 0 ou NaN (colonne vide/zéro) -> INCLURE
                            # 2. Si au moins 5% des valeurs valides sont positives -> INCLURE
                            # 3. Si moins de 5 valeurs valides, inclure automatiquement -> INCLURE
                            if (positive_count == 0) or (positive_count / valid_count >= 0.05) or (valid_count <= 5):
                                numeric_cols.append(col)

                    except:
                        continue

            return numeric_cols

        # Détecter toutes les colonnes numériques
        all_numeric_cols = detect_numeric_columns(df)

        # Colonnes prédéfinies (pour maintenir la compatibilité)
        predefined_cols = ['Salaire des HS', 'Prime de rendement', "Prime d'ancienneté", 'Prime de poste',
                           'Prime de Salissure']

        # Nouvelles colonnes détectées automatiquement
        new_cols = [col for col in all_numeric_cols if col not in predefined_cols]

        # Afficher les nouvelles colonnes détectées
        if new_cols:
            cols_info = []
            for col in new_cols:
                valid_count = pd.to_numeric(df[col], errors='coerce').notna().sum()
                total_rows = len(df)

            cols_text = ", ".join(cols_info)
            st.markdown(f"📊 {cols_text}")

        # Convertir toutes les colonnes numériques
        all_cols_to_process = predefined_cols + new_cols
        for col in all_cols_to_process:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        def safe_sum(df, col):
            """Calcule la somme sécurisée d'une colonne"""
            if col in df.columns:
                numeric_series = pd.to_numeric(df[col], errors='coerce')
                # Retourner la somme même si certaines valeurs sont NaN
                return numeric_series.sum()  # pandas ignore automatiquement les NaN dans sum()
            else:
                return 0

        # Calculs principaux - TOTAUX
        # Colonnes prédéfinies
        total_HS = safe_sum(df, 'Salaire des HS')
        total_prime_rendement = safe_sum(df, 'Prime de rendement')
        total_prime_anciennete = safe_sum(df, "Prime d'ancienneté")
        total_prime_poste = safe_sum(df, 'Prime de poste')
        total_prime_salisseur = safe_sum(df, 'Prime de Salissure')

        # Calculs pour les nouvelles colonnes détectées
        new_cols_totals = {}
        for col in new_cols:
            new_cols_totals[col] = safe_sum(df, col)

        # Total des primes (incluant les nouvelles colonnes)
        total_primes = (
                total_prime_rendement +
                total_prime_anciennete +
                total_prime_poste +
                total_prime_salisseur
        )

        if 'Heures suppl' in df.columns:
            total_nb_HS = df['Heures suppl'].sum()
        else:
            total_nb_HS = 0

        # ===== AFFICHAGE DES MÉTRIQUES =====
        # Première ligne - métriques principales
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
                <div class="paie-metric-card card-rendement">
                    <h3>Nombre total des heures supplémentaires</h3>
                    <p>{total_nb_HS}</p>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="paie-metric-card card-hs">
                    <h3>Montant Total des heures supplémentaires</h3>
                    <p>{total_HS:,.2f} DH</p>
                </div>
                """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class="paie-metric-card card-rendement">
                    <h3>Total Prime de rendement</h3>
                    <p>{total_prime_rendement:,.2f} DH</p>
                </div>
                """, unsafe_allow_html=True)

        # Deuxième ligne - primes prédéfinies
        cols_count = 4 + len(new_cols)  # 4 primes prédéfinies + nouvelles colonnes
        cols = st.columns(min(cols_count, 4))  # Maximum 4 colonnes par ligne

        predefined_data = [
            ("Total Prime d'ancienneté", total_prime_anciennete, "card-anciennete-prime"),
            ("Total Prime de poste", total_prime_poste, "card-poste"),
            ("Total Prime de Salissure", total_prime_salisseur, "card-rendement"),
            ("Total de toutes les primes", total_primes, "card-total-primes")
        ]

        for i, (title, value, card_class) in enumerate(predefined_data):
            with cols[i % len(cols)]:
                st.markdown(f"""
                    <div class="paie-metric-card {card_class}">
                        <h3>{title}</h3>
                        <p>{value:,.2f} DH</p>
                    </div>
                    """, unsafe_allow_html=True)

        # Affichage des nouvelles colonnes détectées
        if new_cols:

            # Organiser en lignes de 3 colonnes maximum
            new_cols_chunked = [new_cols[i:i + 3] for i in range(0, len(new_cols), 3)]

            for chunk in new_cols_chunked:
                cols_new = st.columns(len(chunk))

                for i, col in enumerate(chunk):
                    with cols_new[i]:
                        # Créer un titre formaté
                        formatted_title = col.replace('_', ' ').title()

                        # Informations sur le remplissage de la colonne
                        valid_count = pd.to_numeric(df[col], errors='coerce').notna().sum()
                        total_rows = len(df)
                        fill_percentage = (valid_count / total_rows) * 100

                        # Déterminer la couleur et le style
                        if fill_percentage >= 80:
                            card_class = "card-custom"  # Violet
                            inline_style = ""
                        elif fill_percentage >= 50:
                            card_class = "card-anciennete-prime"  # Bleu
                            inline_style = ""
                        elif fill_percentage >= 20:
                            card_class = ""  # Pas de classe spéciale
                            inline_style = 'style="background: linear-gradient(135deg, #fdcb6e 0%, #f39c12 100%);"'
                        else:
                            card_class = ""
                            inline_style = 'style="background: linear-gradient(135deg, #ff7675 0%, #d63031 100%);"'

                        # Toujours afficher la carte !
                        st.markdown(f"""
                            <div class="paie-metric-card {card_class}" {inline_style}>
                                <h3>{formatted_title}</h3>
                                <p>{new_cols_totals[col]:,.2f} DH</p>
                                <small style="color: #f0f0f0; font-size: 0.8em;">
                                </small>
                            </div>
                        """, unsafe_allow_html=True)

        def plot_pie_primes_styled(df):
            """Graphique en camembert des primes (incluant les nouvelles colonnes)"""
            # Toutes les colonnes de primes (prédéfinies + nouvelles)
            primes = ['Prime de rendement', "Prime d'ancienneté", 'Prime de poste', 'Prime de Salissure']
            primes = [col for col in primes if col in df.columns]

            if not primes:
                st.markdown('<div class="custom-warning">⚠️ Aucune colonne de primes trouvée pour le graphique.</div>',
                            unsafe_allow_html=True)
                return None

            # Calculer les TOTAUX pour chaque prime
            totaux, labels = [], []
            for col in primes:
                total = pd.to_numeric(df[col], errors='coerce').sum()
                # Inclure même les colonnes avec total = 0
                totaux.append(total)
                # Formatter les labels
                label = col.replace('Prime de ', '').replace("Prime d'", '').replace('_', ' ').title()
                labels.append(label)

            # Filtrer seulement les totaux négatifs (cas d'erreur) mais garder les zéros
            valid_indices = [i for i, total in enumerate(totaux) if total >= 0]
            totaux = [totaux[i] for i in valid_indices]
            labels = [labels[i] for i in valid_indices]

            if not totaux:
                st.markdown('<div class="custom-warning">⚠️ Aucune donnée valide pour les primes.</div>',
                            unsafe_allow_html=True)
                return None

            # Si tous les totaux sont à 0, afficher un message spécial
            if all(total == 0 for total in totaux):
                st.markdown('<div class="custom-info">ℹ️ Toutes les colonnes de primes sont à 0 ou vides.</div>',
                            unsafe_allow_html=True)
                # On peut quand même afficher le graphique pour montrer la structure
                # Remplacer les 0 par de très petites valeurs pour la visualisation
                totaux = [0.01 if total == 0 else total for total in totaux]

            st.markdown('<div class="paie-section-header"><h2>Répartition des Primes</h2></div>',
                        unsafe_allow_html=True)

            st.markdown('<div class="chart-container">', unsafe_allow_html=True)

            fig_pr, ax = plt.subplots(figsize=(12, 8))
            fig_pr.patch.set_facecolor('#f0f2f6')

            # Palette de couleurs étendue
            colors = ['#667eea', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#a29bfe', '#fd79a8', '#fdcb6e', '#00b894',
                      '#ff7675'][:len(totaux)]

            # Pie : % seulement
            wedges, texts, autotexts = ax.pie(
                totaux,
                labels=None,
                autopct='%1.1f%%',
                startangle=90,
                colors=colors,
                shadow=True,
                explode=[0.05] * len(totaux),
                textprops={'fontsize': 11, 'fontweight': 'bold'}
            )

            # Rendre % plus visibles
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')

            # Titre avec total général
            ax.set_title(
                f'Répartition de Toutes les Primes\nTotal Général: {sum(totaux):,.0f} DH',
                fontsize=16, fontweight='bold', pad=20
            )

            # Légende détaillée
            ax.legend(labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)

            plt.tight_layout()
            st.pyplot(fig_pr)

            st.markdown('</div>', unsafe_allow_html=True)
            return fig_pr

        # Appel de la fonction
        fig_pr = plot_pie_primes_styled(df)

        # Fusion Paie & Informations Générales
        fig_hs = None
        fig_abs = None

        if uploaded_file:
            try:
                xls = pd.ExcelFile(uploaded_file)
                df_paie = xls.parse("Paie – Données de base")
                df_infos = xls.parse("Informations Générales")

                if 'Noms & Prénoms' in df_paie.columns and 'Noms & Prénoms' in df_infos.columns:
                    df_merge = pd.merge(df_paie, df_infos[['Noms & Prénoms', 'Section']], on='Noms & Prénoms',
                                        how='left')

                    # Heures supplémentaires par Section
                    if 'Heures suppl' in df_merge.columns and 'Section' in df_merge.columns:
                        hs_par_Section = df_merge.groupby('Section')['Heures suppl'].sum().sort_values(ascending=False)

                        st.markdown(
                            '<div class="paie-section-header"><h2> Heures Supplémentaires par Section</h2></div>',
                            unsafe_allow_html=True)

                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)

                        fig_hs, ax = plt.subplots(figsize=(12, 6))
                        fig_hs.patch.set_facecolor('#f0f2f6')
                        ax.set_facecolor('#ffffff')

                        # Dégradé de couleurs pour les barres
                        colors = plt.cm.viridis(np.linspace(0, 1, len(hs_par_Section)))

                        bars = ax.bar(hs_par_Section.index, hs_par_Section.values, color=colors,
                                      edgecolor='white', linewidth=2)

                        # Ajouter les valeurs sur les barres
                        for bar, value in zip(bars, hs_par_Section.values):
                            height = bar.get_height()
                            ax.text(bar.get_x() + bar.get_width() / 2., height + max(hs_par_Section.values) * 0.01,
                                    f'{value:.0f}h', ha='center', va='bottom', fontweight='bold')

                        ax.set_xlabel('Section', fontweight='bold', fontsize=12)
                        ax.set_ylabel('Heures Supplémentaires', fontweight='bold', fontsize=12)
                        ax.set_title('Distribution des Heures Supplémentaires par Section',
                                     fontweight='bold', fontsize=14, pad=20)

                        plt.xticks(rotation=45, ha='right')
                        ax.grid(axis='y', alpha=0.3, linestyle='--')
                        ax.set_axisbelow(True)

                        plt.tight_layout()
                        st.pyplot(fig_hs)

                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown(
                        '<div class="custom-warning">⚠️ Clé \'Noms & Prénoms\' manquante pour la jointure.</div>',
                        unsafe_allow_html=True)

                # Taux d'absentéisme moyen par Section
                if all(col in df_paie.columns for col in
                       ['Jours d\'absences', 'Nbre Jours']) and 'Section' in df_infos.columns:
                    if 'Noms & Prénoms' in df_paie.columns and 'Noms & Prénoms' in df_infos.columns:
                        df_paie['Noms & Prénoms'] = df_paie['Noms & Prénoms'].astype(str).str.strip().str.lower()
                        df_infos['Noms & Prénoms'] = df_infos['Noms & Prénoms'].astype(str).str.strip().str.lower()

                        df_merged = pd.merge(df_paie, df_infos[['Noms & Prénoms', 'Section']], on='Noms & Prénoms',
                                             how='left')

                        # Convertir en numérique
                        df_merged['Nbre Jours'] = pd.to_numeric(df_merged['Nbre Jours'], errors='coerce')
                        df_merged['Jours d\'absences'] = pd.to_numeric(df_merged['Jours d\'absences'], errors='coerce')

                        # Calculer la colonne dans df_merged globalement
                        df_merged['Taux d\'absence (%)'] = (df_merged['Jours d\'absences'] / df_merged[
                            'Nbre Jours']) * 100

                        # Puis filtrer pour garder seulement les lignes valides
                        df_merged_filtered = df_merged[
                            (df_merged['Nbre Jours'] > 0) &
                            (df_merged['Jours d\'absences'].notna()) &
                            (df_merged['Jours d\'absences'] > 0)
                            ]

                        if not df_merged_filtered.empty:

                            absences_Section = df_merged_filtered.groupby('Section')[
                                'Taux d\'absence (%)'].mean().sort_values(ascending=False)

                            absences_Section = df_merged.groupby('Section')['Taux d\'absence (%)'].mean().sort_values(
                                ascending=False)

                            st.markdown(
                                '<div class="paie-section-header"><h2>Taux d\'Absentéisme par Section</h2></div>',
                                unsafe_allow_html=True)

                            # Métriques d'absentéisme
                            col1, col2, col3 = st.columns(3)

                            with col1:
                                taux_global = df_merged['Taux d\'absence (%)'].mean()
                                st.markdown(f"""
                                    <div class="paie-metric-card" style="background: linear-gradient(135deg, #ff7675 0%, #d63031 100%);">
                                        <h3> Taux Global</h3>
                                        <p>{taux_global:.1f}%</p>
                                    </div>
                                    """, unsafe_allow_html=True)

                            with col2:
                                section_max = absences_Section.idxmax()
                                taux_max = absences_Section.max()
                                st.markdown(f"""
                                    <div class="paie-metric-card" style="background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);">
                                        <h3> Section Critique</h3>
                                        <p>{section_max}</p>
                                        <small style="color: #fff; font-size: 0.9em;">{taux_max:.1f}%</small>
                                    </div>
                                    """, unsafe_allow_html=True)

                            with col3:
                                section_min = absences_Section.idxmin()
                                taux_min = absences_Section.min()
                                st.markdown(f"""
                                    <div class="paie-metric-card" style="background: linear-gradient(135deg, #00b894 0%, #00a085 100%);">
                                        <h3>Meilleure Section</h3>
                                        <p>{section_min}</p>
                                        <small style="color: #fff; font-size: 0.9em;">{taux_min:.1f}%</small>
                                    </div>
                                    """, unsafe_allow_html=True)

                            st.markdown('<div class="chart-container">', unsafe_allow_html=True)

                            fig_abs, ax = plt.subplots(figsize=(12, 6))
                            fig_abs.patch.set_facecolor('#f0f2f6')
                            ax.set_facecolor('#ffffff')

                            # Couleurs basées sur le taux (rouge pour élevé, vert pour faible)
                            colors = []
                            for taux in absences_Section.values:
                                if taux > 10:
                                    colors.append('#ff7675')  # Rouge
                                elif taux > 5:
                                    colors.append('#fdcb6e')  # Orange
                                else:
                                    colors.append('#00b894')  # Vert

                            bars = ax.bar(absences_Section.index, absences_Section.values, color=colors,
                                          edgecolor='white', linewidth=2)

                            # Ajouter les valeurs sur les barres
                            for bar, value in zip(bars, absences_Section.values):
                                height = bar.get_height()
                                ax.text(bar.get_x() + bar.get_width() / 2.,
                                        height + max(absences_Section.values) * 0.01,
                                        f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')

                            ax.set_xlabel('Section', fontweight='bold', fontsize=12)
                            ax.set_ylabel('Taux d\'Absence (%)', fontweight='bold', fontsize=12)
                            ax.set_title('Taux d\'Absentéisme Moyen par Section',
                                         fontweight='bold', fontsize=14, pad=20)

                            plt.xticks(rotation=45, ha='right')
                            ax.grid(axis='y', alpha=0.3, linestyle='--')
                            ax.set_axisbelow(True)

                            plt.tight_layout()
                            st.pyplot(fig_abs)

                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            absences_Section = None
                            st.markdown(
                                '<div class="custom-info">ℹ️ La colonne \'Jours d\'absences\' est vide ou n\'a que des zéros.</div>',
                                unsafe_allow_html=True)
                    else:
                        st.markdown(
                            '<div class="custom-error">❌ Colonne \'Noms & Prénoms\' manquante pour fusionner.</div>',
                            unsafe_allow_html=True)
                else:
                    st.markdown(
                        '<div class="custom-warning">⚠️ Colonnes manquantes pour calculer le taux d\'absentéisme.</div>',
                        unsafe_allow_html=True)

            except Exception as e:
                st.markdown(f'<div class="custom-error">❌ Erreur lors du traitement du fichier: {str(e)}</div>',
                            unsafe_allow_html=True)

        import io

        # === 1️⃣ DataFrame Statistiques (ÉTENDU) ===
        stats_data = [
            ('Nombre total des heures supplémentaires', total_nb_HS),
            ('Salaire total des HS', f"{total_HS:,.2f} DH"),
            ('Total Prime de rendement', f"{total_prime_rendement:,.2f} DH"),
            ('Total Prime d\'ancienneté', f"{total_prime_anciennete:,.2f} DH"),
            ('Total Prime de poste', f"{total_prime_poste:,.2f} DH"),
            ('Total Prime de salissure', f"{total_prime_salisseur:,.2f} DH")
        ]

        # Ajouter les nouvelles colonnes aux statistiques
        for col, total in new_cols_totals.items():
            formatted_col_name = f"Total {col.replace('_', ' ').title()}"
            stats_data.append((formatted_col_name, f"{total:,.2f} DH"))

        stats_data.append(('Total de toutes les primes', f"{total_primes:,.2f} DH"))
        stats_data.append(('', ''))  # Ligne vide

        df_stats = pd.DataFrame({
            'Indicateur': [item[0] for item in stats_data],
            'Valeur': [item[1] for item in stats_data]
        })

        # === Calculs absentéisme ===
        if absences_Section is not None and not absences_Section.empty:
            taux_global = df_merged['Taux d\'absence (%)'].mean()
            section_max = absences_Section.idxmax()
            taux_max = absences_Section.max()
            section_min = absences_Section.idxmin()
            taux_min = absences_Section.min()
        else:
            taux_global = 0
            section_max = ''
            taux_max = 0
            section_min = ''
            taux_min = 0

        # === Ajouter aux statistiques ===
        df_stats_abs = pd.DataFrame({
            'Indicateur': [
                'Taux d\'absentéisme global',
                'Section avec taux max',
                'Taux d\'absentéisme max',
                'Section avec taux min',
                'Taux d\'absentéisme min'
            ],
            'Valeur': [
                f"{taux_global:.2f}%",
                section_max,
                f"{taux_max:.2f}%",
                section_min,
                f"{taux_min:.2f}%"
            ]
        })
        df_stats = pd.concat([df_stats, df_stats_abs], ignore_index=True)

        # === 2️⃣ Excel en mémoire ===
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Données brutes', index=False)
            df_stats.to_excel(writer, sheet_name='Statistiques', index=False)

            # Ajouter une feuille avec le détail des nouvelles colonnes
            if new_cols:
                new_cols_data = []
                for col in new_cols:
                    valid_count = pd.to_numeric(df[col], errors='coerce').notna().sum()
                    total_rows = len(df)
                    fill_percentage = (valid_count / total_rows) * 100
                    avg_value = pd.to_numeric(df[col], errors='coerce').mean()

                    new_cols_data.append({
                        'Nouvelle Colonne': col,
                        'Total': f"{new_cols_totals[col]:,.2f} DH",
                        'Nombre d\'entrées valides': valid_count,
                        'Total des lignes': total_rows,
                        'Pourcentage de remplissage': f"{fill_percentage:.1f}%",
                        'Moyenne': f"{avg_value:,.2f} DH" if not pd.isna(avg_value) else "0.00 DH",
                        'Statut': (
                            "Optimal (80%+)" if fill_percentage >= 80 else
                            "Bon (50-79%)" if fill_percentage >= 50 else
                            "Acceptable (20-49%)" if fill_percentage >= 20 else
                            "Attention (<20%)" if fill_percentage > 0 else
                            "Vide (0%)"
                        )
                    })

                df_new_cols_detail = pd.DataFrame(new_cols_data)
                df_new_cols_detail.to_excel(writer, sheet_name='Nouvelles Colonnes', index=False)

            # Feuille Graphiques
            workbook = writer.book
            worksheet_graphs = workbook.add_worksheet('Graphiques')
            writer.sheets['Graphiques'] = worksheet_graphs

            # Liste des figures
            img_bufs = []
            fig_list = [fig for fig in [fig_pr, fig_hs, fig_abs] if fig is not None]

            # Sauvegarde en mémoire
            for fig in fig_list:
                buf = io.BytesIO()
                fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
                buf.seek(0)
                img_bufs.append(buf)

            # Insérer en grille 2 colonnes
            row = 1
            col = 1
            max_col = 2  # Nombre de colonnes

            for i, buf in enumerate(img_bufs):
                worksheet_graphs.insert_image(row, col, f'graph_{i + 1}.png', {
                    'image_data': buf,
                    'x_scale': 0.8,
                    'y_scale': 0.8
                })

                # Passer à la colonne suivante
                col += 8  # Ajuste la largeur pour que ça ne chevauche pas

                # Si on a rempli une ligne, retour à colonne 1, nouvelle ligne
                if (i + 1) % max_col == 0:
                    col = 1
                    row += 20  # Décale vers le bas

        output.seek(0)

        # Message de résumé avant le téléchargement
        total_detected = len(new_cols)
        if total_detected > 0:
            st.markdown(f"""
                <div class="custom-success">
                    <strong>Rapport généré avec succès!</strong><br>
                     {total_detected} nouvelle(s) colonne(s) numérique(s) détectée(s) et intégrée(s)<br>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="custom-info">
                    📋 <strong>Rapport généré avec les colonnes standards</strong><br>
                    ℹ️ Aucune nouvelle colonne numérique détectée
                </div>
                """, unsafe_allow_html=True)

        # Bouton de téléchargement
        st.download_button(
            label="📥 Télécharger le rapport complet",
            data=output,
            file_name='rapport_paie_automatique.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            help="Le rapport inclut toutes les colonnes numériques détectées automatiquement"
        )



        return df_stats, new_cols_totals

    # Appel de la fonction principale
    df_stats, new_cols_totals = process_paie_data(df, uploaded_file)
