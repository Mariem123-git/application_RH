import streamlit as st
from utils import recherche_employe
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import unicodedata

def run(df):
    df_filtered = recherche_employe(df)

    # CSS personnalisé pour styliser l'application
    st.markdown("""
            <style>
                /* Style général */
                .main {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 2rem;
                }

                /* Cartes métriques stylisées */
                .metric-card {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px;
                    border-radius: 15px;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                    text-align: center;
                    margin: 10px;
                    border: 1px solid rgba(255,255,255,0.2);
                }

                .metric-card h3 {
                    color: white;
                    margin-bottom: 10px;
                    font-size: 1.2em;
                    font-weight: bold;
                }

                .metric-card p {
                    color: #f0f0f0;
                    font-size: 2em;
                    margin: 0;
                    font-weight: bold;
                }

                /* Cartes colorées spécifiques */
                .card-effectif {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }

                .card-age {
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                }

                .card-anciennete {
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                }

                .card-retraite {
                    background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                }

                .card-feminisation {
                    background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                }

                .card-direct {
                    background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                }

                .card-indirect {
                    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                }

                /* Sections avec fond coloré */
                .section-header {
                    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px;
                    border-radius: 10px;
                    margin: 20px 0;
                    text-align: center;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                }

                /* Métriques d'ancienneté */
                .anc-nouveaux {
                    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                    color: #333;
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    margin: 5px;
                }

                .anc-jeunes {
                    background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%);
                    color: #333;
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    margin: 5px;
                }

                .anc-exp {
                    background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
                    color: #333;
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    margin: 5px;
                }

                .anc-seniors {
                    background: linear-gradient(135deg, #fdbb2d 0%, #22c1c3 100%);
                    color: #333;
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    margin: 5px;
                }

                /* Tableaux stylisés */
                .dataframe {
                    background: rgba(255,255,255,0.9);
                    border-radius: 10px;
                    padding: 10px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                }

                /* Expander stylisé */
                .streamlit-expanderHeader {
                    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border-radius: 10px;
                }
            </style>
        """, unsafe_allow_html=True)

    def normalize(text):
        if pd.isna(text):
            return ""
        text = str(text).upper().replace(" ", "")
        text = ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
        return text

    def classify_direct_indirect_by_section(section):
        if pd.isna(section):
            return "Non classé"
        section_str = normalize(section)
        sections_direct = [
            'MODELAGE', 'COULAGE MOULE', 'PPE', 'COULAGE', 'EMAILLAGE', 'PACKAGING',
            'FOUR-TRIAGE', 'EMBALLAGE', 'QUALITE', 'MG', 'M.G','Moyens Generaux','Magasins matieres premieres','Magasins négoces & accessoirs','Magasins produits finis',
            'ENTRETIEN', 'MAGASINS', 'MCM', 'C. QUALITE', 'PRODUCTION', 'DT', 'LOG', 'PROD', 'P.P.E', 'M.C.M', 'D.T','Qualité H S E','B.E.M.I',
            'C. Qualité','Sechoir','Triage & Contrôle','Reparations','Reparations à Froid','Nettoyage Surfaces','Chauffeurs','Gardiens','Jardinage','Laboratoires','Recherches et developpement C.A.O/F.A.O'
        ]
        sections_indirect = [
            'ACHATS', 'RH', 'INFORMATIQUE', 'COMPTABILITE', 'DIRECTION', 'R.H','Gestion Comptables','Contrôle de Gestion','Gestion du Personnel & Paie','Assistance Suivi Sociale & Contrats'
            'CADRES NON DECLARES', 'ASSISTANTS', 'ADM', 'DG', 'COMPTABILITÉ', 'INFORMATIQUE', 'D.G','SOFT','HARD','DATA SECRURITY','ASSISTANTS'
        ]

        for section_direct in sections_direct:
            if normalize(section_direct) in section_str:
                return "Direct"
        for section_indirect in sections_indirect:
            if normalize(section_indirect) in section_str:
                return "Indirect"

        return "Non classé"

    def process_data(df):
        if df.empty:
            st.error("Le DataFrame est vide.")
            return

        # Traitement des dates
        if 'Date d\'embauche' in df.columns:
            df['Date d\'embauche'] = pd.to_datetime(df['Date d\'embauche'], errors='coerce')
            df['Ancienneté'] = (pd.Timestamp('today') - df['Date d\'embauche']).dt.days // 365
            df['Ancienneté'] = df['Ancienneté'].fillna(0)  # Remplacer NaN par 0

        if 'Date de naissance' in df.columns:
            df['Date de naissance'] = pd.to_datetime(df['Date de naissance'], errors='coerce')
            df['Âge'] = (pd.Timestamp('today') - df['Date de naissance']).dt.days // 365
            df['Âge'] = df['Âge'].fillna(0)  # Remplacer NaN par 0

        # Calculer les statistiques générales
        effectif = len(df)

        anciennete_moy = df['Ancienneté'].mean() if 'Ancienneté' in df.columns else 0
        age_moyen = df['Âge'].mean() if 'Âge' in df.columns else 0
        nb_proches = len(df[df['Âge'] >= 56]) if 'Âge' in df.columns else 0
        colonne_sortie = next((c for c in df.columns if 'date' in c.lower() and 'sortie' in c.lower()), None)

        if colonne_sortie:
            df[colonne_sortie] = pd.to_datetime(df[colonne_sortie], errors='coerce')
            df['Mois sortie'] = df[colonne_sortie].dt.month
            nb_depart = df[df[colonne_sortie].notna()].shape[0]
        else:
            nb_depart = 0
        # ✅ Calcul du turnover
        turnover = (nb_depart / effectif) * 100 if effectif > 0 else 0

        colonne_section = next((c for c in df.columns if c.lower().strip() in ['section', 'Section', 'SECTION']), None)
        if colonne_section:
            df['Classification_DI'] = df[colonne_section].apply(classify_direct_indirect_by_section)
            nb_direct = len(df[df['Classification_DI'] == 'Direct'])
            nb_indirect = len(df[df['Classification_DI'] == 'Indirect'])
        else:
            nb_direct = nb_indirect = 0

        sexe_col = next((c for c in df.columns if c.lower().strip() == 'sexe'), None)

        # Cartes métriques stylisées
        st.markdown('<div class="section-header"><h2>Des statistiques</h2></div>', unsafe_allow_html=True)

        # Première ligne de métriques
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(f"""
                    <div class="metric-card card-feminisation">
                        <h3>Total Effectifs</h3>
                        <p>{effectif}</p>
                    </div>
                """, unsafe_allow_html=True)

        with col2:
            if 'Âge' in df.columns:
                age_moyen = df['Âge'].mean()
                st.markdown(f"""
                        <div class="metric-card card-age">
                            <h3>Âge Moyen</h3>
                            <p>{age_moyen:.1f} ans</p>
                        </div>
                    """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                    <div class="metric-card card-anciennete">
                        <h3>Ancienneté Moyenne</h3>
                        <p>{anciennete_moy:.1f} ans</p>
                    </div>
                """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
                    <div class="metric-card card-retraite">
                        <h3>Proches Retraite</h3>
                        <p>{nb_proches}</p>
                    </div>
                """, unsafe_allow_html=True)
        with col5:
            st.markdown(f"""
                      <div class="metric-card card-retraite">
                             <h3>Départs prévus par mois</h3>
                             <p>{nb_depart}</p>
                      </div>
                """, unsafe_allow_html=True)

        # Deuxième ligne de métriques (Direct/Indirect + Féminisation)

        col4, col5, col6, col7 = st.columns(4)
        with col4:
            st.markdown(f"""
                        <div class="metric-card">
                           <h3>Direct</h3>
                           <p>{nb_direct}</p>
                        </div>
                    """, unsafe_allow_html=True)
        with col5:
            st.markdown(f"""
                        <div class="metric-card">
                            <h3>Indirect</h3>
                            <p>{nb_indirect}</p>
                        </div>
                    """, unsafe_allow_html=True)
        with col6:
            if sexe_col:
                valeurs_feminines = ['Femme', 'F', 'Female', 'Féminin']
                total_femmes = sum(df[sexe_col].value_counts().get(v, 0) for v in valeurs_feminines)
                ratio_femmes = (total_femmes / len(df)) * 100 if len(df) > 0 else 0
                st.markdown(f"""
                            <div class="metric-card card-feminisation">
                                <h3>Taux de Féminisation</h3>
                                <p>{ratio_femmes:.1f}%</p>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                            <div class="metric-card card-feminisation">
                                <h3>Taux de Féminisation</h3>
                                <p>Non disponible</p>
                            </div>
                        """, unsafe_allow_html=True)
        with col7:
            st.markdown(f"""
                        <div class="metric-card card-anciennete">
                            <h3> Taux de Turnover</h3>
                            <p>{turnover:.2f}%</p>
                        </div>
                    """, unsafe_allow_html=True)

        # Section des proches retraite
        if 'Date de naissance' in df.columns:
            df['Date de sortie'] = df['Date de naissance'] + pd.to_timedelta(60 * 365.25, unit='D')
            # assurer que la colonne est au bon format datetime
            df['Date de sortie'] = df['Date de sortie'].dt.strftime('%d/%m/%Y')
            df['Date d\'embauche'] = df['Date d\'embauche'].dt.strftime('%d/%m/%Y')

        cols_base = ['Matricule', 'Noms & Prénoms', 'Âge', 'Date d\'embauche', 'Date de sortie', 'Ancienneté',
                     'Departement',
                     'Section', 'Fonction']

        cols = [c for c in cols_base if c in df.columns]
        if nb_proches > 0:
            st.markdown('<div class="section-header"><h2> Proches Retraite</h2></div>', unsafe_allow_html=True)
            if cols:
                with st.expander("Voir liste proches retraite"):
                    proches_retraite = df[df['Âge'] >= 56][cols].sort_values(by='Âge', ascending=False)
                    st.dataframe(proches_retraite, use_container_width=True)

        # CSP - Catégories Socioprofessionnelles
        csp_mapping = {
            "Directeur": ["Directeur", "Président"],
            "Manager": ["Manager", "Chef du personnel", "Chef Département PPE", "Responsable Maintenance",
                        "Responsable Achats & Sourcing", "Resp de la Création et du Développement de PS",
                        "Resp de l'Electromécanique & des Machines à Commandes Numériques"," Conseiller Technique Responsable de la Création et du Développement de Produits Sanitaires",
                        "Responsable d'Agence", "Responsable Système d'Information & Projets",
                        "Resp Projet Informatisation", "Resp SQH Sécurité et Environnement"],
            "Manager Moyen": ["Manager Moyen", "Chef d'Equipe Coulage", "Chef d'Equipe Fours",
                              "Chef d'Equipe Réparation", "Chef d'Equipe Emaillage",
                              "Chef d'Equipe Coulage Moule", "Chef de Coulage"],
            "Technicien assistant": ["Technicien assistant"],
            "Technicien de Maintenance": ["Technicien de Maintenance"],
            "Technicien": ["Technicien", "Chaudronnier", "Agent de Méthodes", "Agent de Laboratoire de PPE",
                           "Agent de Laboratoire de P.P.E",
                           "Qualiticienne", "Agent de Qualité", "Agent de Bureau"],
            "Modeleur": ["Modeleur"],
            "Matriceur": ["Matriceur"],
            "Trieur": ["Trieur"],
            "Auditeur": ["Auditeur"],
            "Operateur": ["Operateur", "Ouvrier", "Opérateur PPE","Opérateur P.P.E" ,"Operateur Qualifie"],
            "Chauffeur": ["Chauffeur"],
            "Gardien": ["Gardien"],
            "Cadre administratif": ["Cadre administratif", "Responsable Juridique", "Comptable",
                                    "Contrôleur de Gestion", "Acheteuse"],
            "Employé": ["employe(e)", "Magasinier Expédition", "Ouvrière Ménage et Cuisine", "Ouvrière Ménage",
                        "Préparateur Commande & Emballage", "Aide Magasinier", "Réparation des Palettes",
                        "Magasinier", "Aide Comptable"],
            "Agent de maintenance": ["Agent de maintenance"],
            "Agent de maitrise": ["Agent de maitrise"],
            "Stagiaire": ["Stagiaire"]
        }

        def get_csp(fonction):
            if pd.isna(fonction):
                return "Non classé"

            fonction_lower = str(fonction).lower()
            for csp, mots in csp_mapping.items():
                for mot in mots:
                    if mot.lower() in fonction_lower:
                        return csp
            return "Non classé"

        if 'Fonction' in df.columns:
            df['CSP'] = df['Fonction'].apply(get_csp)
            csp_effectif = df.groupby('CSP').size().reset_index(name='Effectif')

            st.markdown('<div class="section-header"><h2>📋 Analyse des CSP</h2></div>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📊 Effectif par CSP")
                st.dataframe(csp_effectif, use_container_width=True, height=400)

            with col2:
                csp_fonc = df.groupby('CSP')['Fonction'].unique().reset_index().rename(
                    columns={'CSP': 'Catégorie Socioprofessionnelle', 'Fonction': 'Fonctions associées'}
                )
                csp_fonc['Fonctions associées'] = csp_fonc['Fonctions associées'].apply(
                    lambda arr: "\n• " + "\n• ".join(arr) if len(arr) > 0 else ""
                )
                st.subheader("📋 Fonctions par CSP")
                st.dataframe(csp_fonc, use_container_width=True, height=400)

            # Graphique CSP
            st.markdown('<div class="section-header"><h2>📊 Répartition par CSP</h2></div>', unsafe_allow_html=True)

            fig_csp, ax = plt.subplots(figsize=(12, 8))
            fig_csp.patch.set_facecolor('#f0f2f6')
            ax.set_facecolor('#ffffff')

            colors = plt.cm.viridis(np.linspace(0, 1, len(csp_effectif)))
            bars = ax.barh(csp_effectif['CSP'], csp_effectif['Effectif'], color=colors)

            for bar, effectif in zip(bars, csp_effectif['Effectif']):
                ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                        f'{effectif}', ha='left', va='center', fontweight='bold', fontsize=11)

            ax.set_xlabel('Effectif', fontweight='bold', fontsize=12)
            ax.set_ylabel('Catégorie Socioprofessionnelle', fontweight='bold', fontsize=12)
            ax.set_title('Distribution des Effectifs par CSP', fontweight='bold', fontsize=14, pad=20)
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            ax.set_axisbelow(True)

            plt.tight_layout()
            st.pyplot(fig_csp)

        # Graphique Âge & Sexe
        if sexe_col and 'Âge' in df.columns:
            st.markdown('<div class="section-header"><h2>📊 Répartition par Âge et Sexe</h2></div>',
                        unsafe_allow_html=True)

            bins_age = [0, 25, 35, 45, 55, 65, 100]
            labels_age = ['<25', '25-34', '35-44', '45-54', '55-64', '65+']
            df['Tranche Âge'] = pd.cut(df['Âge'], bins=bins_age, labels=labels_age, right=False)
            age_sexe = df.groupby(['Tranche Âge', sexe_col]).size().reset_index(name='Effectif')

            col1, col2 = st.columns(2)

            with col1:
                fig_age_bar, ax = plt.subplots(figsize=(10, 6))
                fig_age_bar.patch.set_facecolor('#f0f2f6')
                ax.set_facecolor('#ffffff')

                palette = {
                    "Homme": "#2E86AB", "Femme": "#A23B72",
                    "M": "#2E86AB", "F": "#A23B72",
                    "H": "#2E86AB", "Male": "#2E86AB", "Female": "#A23B72",
                    "Masculin": "#2E86AB", "Féminin": "#A23B72"
                }

                bars = sns.barplot(data=age_sexe, x="Tranche Âge", y="Effectif", hue=sexe_col, palette=palette, ax=ax)

                for container in ax.containers:
                    ax.bar_label(container, fontweight='bold', fontsize=10)

                ax.set_xlabel('Tranches d\'âge', fontweight='bold', fontsize=12)
                ax.set_ylabel('Effectif', fontweight='bold', fontsize=12)
                ax.set_title('Répartition par Âge et Sexe', fontweight='bold', fontsize=14, pad=20)
                ax.legend(title='Sexe', title_fontsize=12, fontsize=11, loc='upper right')
                ax.grid(axis='y', alpha=0.3, linestyle='--')
                ax.set_axisbelow(True)

                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig_age_bar)
            with col2:
                pivot_age = age_sexe.pivot(index='Tranche Âge', columns=sexe_col, values='Effectif').fillna(0)

                fig_age_area, ax = plt.subplots(figsize=(10, 6))
                fig_age_area.patch.set_facecolor('#f0f2f6')
                ax.set_facecolor('#ffffff')

                colors = []
                for col in pivot_age.columns:
                    if col in palette:
                        colors.append(palette[col])
                    else:
                        colors.append("#999999")

                pivot_age.plot.area(ax=ax, color=colors, alpha=0.7, stacked=True)
                ax.set_xlabel('Tranches d\'âge', fontweight='bold', fontsize=12)
                ax.set_ylabel('Effectif', fontweight='bold', fontsize=12)
                ax.set_title('Évolution par Tranches d\'Âge', fontweight='bold', fontsize=14, pad=20)
                ax.legend(title='Sexe', title_fontsize=12, fontsize=11, loc='upper right')
                ax.grid(alpha=0.3, linestyle='--')
                ax.set_axisbelow(True)

                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig_age_area)
        # Graphique Ancienneté
        if 'Ancienneté' in df.columns:
            st.markdown('<div class="section-header"><h2>📊 Analyse de l\'Ancienneté</h2></div>', unsafe_allow_html=True)

            bins_anc = [0, 1, 4, 7, 10, 13, 16, 20, 23]
            labels_anc = ['<1 an', '1-3 ans', '4-6 ans', '7-9 ans', '10-12 ans',
                          '13-15 ans', '16-19 ans', '20-22 ans']
            df['Tranche Ancienneté'] = pd.cut(df['Ancienneté'], bins=bins_anc,
                                              labels=labels_anc, right=False)
            anc_grp = df['Tranche Ancienneté'].value_counts().sort_index().reset_index()
            anc_grp.columns = ['Tranche Ancienneté', 'Effectif']

            # Métriques d'ancienneté stylisées
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                nouveaux = anc_grp[anc_grp['Tranche Ancienneté'] == '<1 an']['Effectif'].sum()
                st.markdown(f"""
                      <div class="anc-nouveaux">
                          <h3> Nouveaux (<1 an)</h3>
                          <h2>{nouveaux}</h2>
                      </div>
                      """, unsafe_allow_html=True)

            with col2:
                jeunes = anc_grp[anc_grp['Tranche Ancienneté'].isin(['1-3 ans', '4-6 ans'])]['Effectif'].sum()
                st.markdown(f"""
                      <div class="anc-jeunes">
                          <h3> Jeunes (1-6 ans)</h3>
                          <h2>{jeunes}</h2>
                      </div>
                      """, unsafe_allow_html=True)

            with col3:
                expérimentés = anc_grp[anc_grp['Tranche Ancienneté'].isin(['7-9 ans', '10-12 ans'])]['Effectif'].sum()
                st.markdown(f"""
                      <div class="anc-exp">
                          <h3> Expérimentés (7-12 ans)</h3>
                          <h2>{expérimentés}</h2>
                      </div>
                      """, unsafe_allow_html=True)

            with col4:
                seniors = anc_grp[anc_grp['Tranche Ancienneté'].isin(['13-15 ans', '16-19 ans', '20-22 ans'])][
                    'Effectif'].sum()
                st.markdown(f"""
                      <div class="anc-seniors">
                          <h3> Seniors (13+ ans)</h3>
                          <h2>{seniors}</h2>
                      </div>
                      """, unsafe_allow_html=True)

            # Graphique principal d'ancienneté
            fig_anciennete, ax = plt.subplots(figsize=(14, 8))
            fig_anciennete.patch.set_facecolor('#f0f2f6')
            ax.set_facecolor('#ffffff')

            colors = plt.cm.plasma(np.linspace(0, 1, len(anc_grp)))
            bars = ax.bar(anc_grp['Tranche Ancienneté'], anc_grp['Effectif'],
                          color=colors, edgecolor='white', linewidth=2)

            for bar, effectif in zip(bars, anc_grp['Effectif']):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                        f'{effectif}', ha='center', va='bottom', fontweight='bold', fontsize=12)

            ax.set_xlabel('Tranches d\'ancienneté', fontweight='bold', fontsize=12)
            ax.set_ylabel('Effectif', fontweight='bold', fontsize=12)
            ax.set_title('Distribution des Effectifs par Ancienneté', fontweight='bold', fontsize=16, pad=20)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.set_axisbelow(True)

            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig_anciennete)

        # Tableau détaillé par section
        st.markdown('<div class="section-header"><h3>📋 Effectifs direct et indirect par section</h3></div>',
                    unsafe_allow_html=True)

        # Création du tableau général
        section_summary = df.groupby([colonne_section, 'Classification_DI']).size().unstack(fill_value=0)

        # 1️⃣ Tableau Direct uniquement
        section_direct = section_summary[section_summary['Direct'] > 0][['Direct']].copy()
        section_direct = section_direct.reset_index()  # remettre la section en colonne
        section_direct = section_direct[[colonne_section, 'Direct']]
        section_direct = section_direct.rename(
            columns={colonne_section: 'Section', 'Direct': 'Effectif Direct'})

        # Ajouter une ligne TOTAL
        total_direct = pd.DataFrame({
            'Section': ['TOTAL'],
            'Effectif Direct': [section_direct['Effectif Direct'].sum()]
        })
        section_direct = pd.concat([section_direct, total_direct], ignore_index=True)

        # 2️⃣ Tableau Indirect uniquement
        section_indirect = section_summary[section_summary['Indirect'] > 0][['Indirect']].copy()
        section_indirect = section_indirect.reset_index()
        section_indirect = section_indirect[[colonne_section, 'Indirect']]
        section_indirect = section_indirect.rename(
            columns={colonne_section: 'Section', 'Indirect': 'Effectif Indirect'})

        # Ajouter une ligne TOTAL
        total_indirect = pd.DataFrame({
            'Section': ['TOTAL'],
            'Effectif Indirect': [section_indirect['Effectif Indirect'].sum()]
        })
        section_indirect = pd.concat([section_indirect, total_indirect], ignore_index=True)

        # 👉 Afficher côte à côte
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📋 Tableau des sections Direct")
            st.dataframe(
                section_direct.style.background_gradient(cmap='Greens'),
                use_container_width=True
            )

        with col2:
            st.markdown("### 📋 Tableau des sections Indirect")
            st.dataframe(
                section_indirect.style.background_gradient(cmap='Oranges'),
                use_container_width=True
            )

        # Graphique en barres pour Direct vs Indirect
        st.markdown('<div class="section-header"><h3>📊 Comparaison Direct vs Indirect</h3></div>',
                    unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])

        with col1:

            fig_direct_indirect, ax = plt.subplots(figsize=(12, 8))
            fig_direct_indirect.patch.set_facecolor('#f0f2f6')
            ax.set_facecolor('#ffffff')

        # Préparer les données pour le graphique
        categories = ['Personnel Direct', 'Personnel Indirect']
        effectifs = [nb_direct, nb_indirect]
        colors = ['#ff6b6b', '#4ecdc4']

        # Créer les barres
        bars = ax.bar(categories, effectifs, color=colors, edgecolor='white', linewidth=3, alpha=0.8,
                      width=0.6)

        # Ajouter les valeurs sur les barres
        for bar, effectif in zip(bars, effectifs):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + max(effectifs) * 0.01,
                    f'{effectif}', ha='center', va='bottom', fontweight='bold', fontsize=16, color='#333')

            # Styliser le graphique
            ax.set_ylabel('Nombre d\'employés', fontweight='bold', fontsize=14)
            ax.set_title('Comparaison Effectifs Direct vs Indirect', fontweight='bold', fontsize=16, pad=20)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            ax.set_axisbelow(True)

            # Ajuster les limites de l'axe y
            ax.set_ylim(0, max(effectifs) * 1.15)

        # Ajouter des annotations de pourcentage
        effectif_total = sum(effectifs)
        for i, (bar, effectif) in enumerate(zip(bars, effectifs)):
            percentage = (effectif / effectif_total) * 100 if effectif_total > 0 else 0
            ax.text(bar.get_x() + bar.get_width() / 2., effectif / 2,
                    f'{percentage:.1f}%', ha='center', va='center',
                    fontweight='bold', fontsize=14, color='white')

        plt.tight_layout()
        st.pyplot(fig_direct_indirect)
        # Graphe effectif par service
        st.markdown('<div class="section-header"><h3>📊Effectif par section</h3></div>',
                    unsafe_allow_html=True)
        section_plot = section_summary.reset_index()
        section_plot = section_plot[[colonne_section, 'Direct', 'Indirect']]
        fig_section, ax = plt.subplots(figsize=(12, 7))
        fig_section.patch.set_facecolor('#f0f2f6')
        ax.set_facecolor('#ffffff')

        bar_width = 0.35
        index = np.arange(len(section_plot))
        bars1 = ax.bar(index, section_plot['Direct'], bar_width, label='Direct', color='#4CAF50')
        bars2 = ax.bar(index + bar_width, section_plot['Indirect'], bar_width, label='Indirect', color='#FF9800')

        # Ajout des labels de section sur l'axe x
        ax.set_xlabel('Section', fontweight='bold')
        ax.set_ylabel('Effectif', fontweight='bold')
        ax.set_title('Effectif par section', fontweight='bold', fontsize=14, pad=20)
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(section_plot[colonne_section], rotation=45, ha='right')

        # Affichage des valeurs sur les barres
        for bar in bars1:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f'{int(height)}', ha='center', va='bottom',
                        fontsize=9)

        for bar in bars2:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f'{int(height)}', ha='center', va='bottom',
                        fontsize=9)

        ax.legend()
        ax.grid(axis='y', alpha=0.3, linestyle='--')

        plt.tight_layout()
        st.pyplot(fig_section)




        # Vérifier si la colonne 'Département' existe

        df.columns = df.columns.str.strip().str.lower()
        if 'departement' in df.columns :

            st.markdown('<div class="section-header"><h2>📊 Effectif par Département</h2></div>',
                        unsafe_allow_html=True)

            # Nettoyer : enlever espaces
            df['departement'] = df['departement'].astype(str).str.strip()

            # Compter effectif
            effectif_dept = df['departement'].value_counts().sort_values(ascending=False)

            if not effectif_dept.empty:
                fig_dept, ax = plt.subplots(figsize=(12, 6))
                fig_dept.patch.set_facecolor('#f0f2f6')
                ax.set_facecolor('#ffffff')

                # Dégradé de couleurs
                colors = plt.cm.tab20(np.linspace(0, 1, len(effectif_dept)))

                bars = ax.bar(effectif_dept.index, effectif_dept.values, color=colors, edgecolor='white')

                # Ajouter valeurs sur les barres
                for bar, count in zip(bars, effectif_dept.values):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width() / 2., height + max(effectif_dept.values) * 0.01,
                            f'{count}', ha='center', va='bottom', fontweight='bold')

                ax.set_xlabel('departement', fontweight='bold', fontsize=12)
                ax.set_ylabel('Effectif', fontweight='bold', fontsize=12)
                ax.set_title('Effectif par Département', fontweight='bold', fontsize=14, pad=20)

                plt.xticks(rotation=45, ha='right')
                ax.grid(axis='y', alpha=0.3, linestyle='--')
                ax.set_axisbelow(True)

                plt.tight_layout()
                st.pyplot(fig_dept)

            else:
                st.info("ℹ️ Aucun département trouvé pour l'analyse.")
        else:
            st.warning("⚠️ La colonne 'Département' est manquante.")

        # Graphique Type de contrat
        if 'ancienneté' in df.columns:
            if 'type de contrat' not in df.columns:
                df['type de contrat'] = None  # Créer la colonne vide si elle n'existe pas

            # Vérifier si la colonne Type de contrat est majoritairement vide
            contrats_non_vides = df['type de contrat'].notna().sum()
            total_lignes = len(df)

            # Si moins de 10% des valeurs sont remplies, considérer comme vide
            colonne_vide = (contrats_non_vides / total_lignes) < 0.1

            if colonne_vide:
                # CAS 1: Colonne vide - Remplir automatiquement selon l'ancienneté
                st.info("📝 Génération automatique des types de contrat basée sur l'ancienneté")
                df.loc[df['ancienneté'] >= 1, 'type de contrat'] = 'CDI'
                df.loc[df['ancienneté'] < 1, 'type de contrat'] = 'CDD'
                contrats_valides = ['CDD', 'CDI']
            else:
                # CAS 2: Colonne remplie - Utiliser tous les types possibles
                st.info("📋 Utilisation des types de contrat existants dans les données")
                contrats_valides = ['CDD', 'CDI', 'CTE', 'ANAPEC', 'STAGE']

            # Filtrer selon les contrats valides
            df_filtre = df[df['type de contrat'].isin(contrats_valides)]

            if 'type de contrat' in df_filtre.columns:
                st.markdown('<div class="section-header"><h2>📊 Répartition par Type de Contrat</h2></div>',
                            unsafe_allow_html=True)

                contrats = df_filtre['type de contrat'].value_counts()

                if len(contrats) > 0:
                    col1, col2 = st.columns([1, 2])

                    with col1:
                        fig_contrat, ax = plt.subplots(figsize=(6, 6))
                        fig_contrat.patch.set_facecolor('#f0f2f6')

                        colors = plt.cm.Set3(np.linspace(0, 1, len(contrats)))
                        ax.pie(
                            contrats.values,
                            labels=contrats.index,
                            autopct='%1.1f%%',
                            startangle=140,
                            colors=colors,
                            shadow=True,
                            explode=[0.05] * len(contrats)
                        )
                        ax.set_title('Répartition par Type de Contrat', fontweight='bold', fontsize=14, pad=20)
                        st.pyplot(fig_contrat)

                    with col2:
                        st.markdown("### 📋 Détail des contrats")
                        for i, (contrat, count) in enumerate(contrats.items()):
                            color = plt.cm.Set3(i / len(contrats))
                            color_hex = '#%02x%02x%02x' % (int(color[0] * 255), int(color[1] * 255),
                                                           int(color[2] * 255))

                            st.markdown(f"""
                                  <div style="
                                      background: {color_hex};
                                      padding: 15px;
                                      border-radius: 10px;
                                      margin: 10px 0;
                                      text-align: center;
                                      box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                                  ">
                                      <h3 style="margin: 0; color: #333;">{contrat}</h3>
                                      <h2 style="margin: 5px 0; color: #333;">{count}</h2>
                                  </div>
                                  """, unsafe_allow_html=True)
                else:
                    st.info("ℹ️ Aucun contrat trouvé pour l'analyse.")
            else:
                st.warning("⚠️ La colonne 'Type de contrat' est manquante.")
        else:
            st.warning("⚠️ La colonne 'Ancienneté' est manquante pour générer les types de contrat.")
        import io

        # ✅ 1️⃣ Crée un DataFrame directement depuis tes stats déjà calculées
        df_stats = pd.DataFrame({
            'Indicateur': [
                'Effectif total',
                'Âge moyen',
                'Ancienneté moyenne',
                'Proches Retraite',
                'Départs prévus',
                'Turnover',
                'Effectif Direct',
                'Effectif Indirect'
            ],
            'Valeur': [
                effectif,
                round(age_moyen, 1) if 'Âge' in df.columns else 0,
                round(anciennete_moy, 1) if 'Ancienneté' in df.columns else 0,
                nb_proches,
                nb_depart,
                turnover,
                nb_direct,
                nb_indirect
            ]
        })

        # ✅ 2️⃣ Mets le DataFrame dans un fichier Excel en mémoire
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Données brutes', index=False)
            df_stats.to_excel(writer, sheet_name='Statistiques', index=False)
            if nb_proches > 0:
                proches_retraite.to_excel(writer, sheet_name='Proches Retraite', index=False)
            sheet_name = 'Direct_Indirect'
            section_direct.to_excel(writer, sheet_name=sheet_name, index=False, startrow=0, startcol=0)
            startcol_indirect = len(section_direct.columns) + 3
            section_indirect.to_excel(writer, sheet_name=sheet_name, index=False, startrow=0,
                                      startcol=startcol_indirect)

            Sheet_name = 'CSP'
            csp_effectif.to_excel(writer, sheet_name=Sheet_name, index=False, startrow=0, startcol=0)
            startcol_csp = len(csp_effectif.columns) + 3
            csp_fonc.to_excel(writer, sheet_name=Sheet_name, index=False, startrow=0, startcol=startcol_csp)

            workbook = writer.book
            worksheet_graphs = workbook.add_worksheet('Graphiques')
            writer.sheets['Graphiques'] = worksheet_graphs

            img_bufs = []
            fig_list = [
                fig_csp,
                fig_age_bar,
                fig_age_area,
                fig_anciennete,
                fig_direct_indirect,
                fig_section,
                fig_dept,
                fig_contrat

            ]
            if 'Type de contrat' in df.columns:
                fig_list.append(fig_contrat)
            fig_list.append(fig_csp)

            for fig in fig_list:
                buf = io.BytesIO()
                fig.savefig(buf, format='png')
                buf.seek(0)
                img_bufs.append(buf)
            row = 40
            col = 10
            for i, buf in enumerate(img_bufs):
                cell = f'A{row}'
                worksheet_graphs.insert_image(cell, f'graphe_{i + 1}.png',
                                              {'image_data': buf, 'x_scale': 0.8, 'y_scale': 0.8})
                row += 20

        output.seek(0)

        # ✅ 3️⃣ Ajoute le bouton de téléchargement
        st.download_button(
            label="📥 Télécharger les statistiques Excel",
            data=output,
            file_name='Statistiques_RH.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    process_data(df)

