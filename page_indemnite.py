from utils import recherche_employe
from uploader import uploader_excel
import pandas as pd
import streamlit as st


def run(df):
    import streamlit as st
    import pandas as pd

    st.markdown("""
    <div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 50%,#f093fb 100%);
                padding: 25px; border-radius:15px;margin-bottom:30px;
                box-shadow: 0 10px 30px rgba(102,126,234,0.3);
                border: 1px solid rgba(255,255,255,0.1);">
          <h1 style="color:white;text-align:center;margin:0;
                     text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                     font-size: 2.5em;">
                Indemnités & Avantages
          </h1>
          <p style="color:white;text-align:center;margin:15px 0 0 0;opacity:0.9;
                    font-size: 1.1em;">
                Analyse détaillée des indemnités et avantages accordés aux employés
          </p>
    </div>
        """, unsafe_allow_html=True)

    df_filtered = recherche_employe(df)
    use_filtered = st.checkbox("Utiliser le filtre pour les graphiques", value=False)
    if use_filtered and df_filtered is not None:
        df = df_filtered

    df.columns = [col.strip().lower() for col in df.columns]
    df = df.iloc[:-1, :]

    indemnites_config = {
        'indemnité de licenciement': {'color': '#ff6b6b', 'bg': '#ffe5e5'},
        'indemnité de transport': {'color': '#4ecdc4', 'bg': '#e5f9f7'},
        'indemnite de déplacement': {'color': '#445b7d', 'bg': '#e8ebf0'},
        'indemnite de représentation': {'color': '#96ceb4', 'bg': '#f0f8f5'},
        'indemnité de panier': {'color': '#feca57', 'bg': '#fff9e5'},
        'voiture': {'color': '#ff9ff3', 'bg': '#fef5fe'}
    }

    stats = {}
    indemnites_data = []

    for config_col, config in indemnites_config.items():
        for df_col in df.columns:
            if config_col.strip().lower() == df_col.strip().lower():
                serie = pd.to_numeric(df[df_col], errors='coerce').dropna()
                if not serie.empty:
                    total = serie.sum()
                    moyenne = serie.mean()
                    nb_employes = (serie > 0).sum()
                    pourcentage_beneficiaires = (nb_employes / len(df)) * 100 if len(df) > 0 else 0

                    # Garder seulement les statistiques essentielles
                    stats[config_col] = {
                        'Total': total,
                        'Moyenne': moyenne,
                        'Nombre des employés concernés': nb_employes,
                        'Pourcentage de bénéficiaires': pourcentage_beneficiaires,
                        'color': config['color'],
                        'bg': config['bg']
                    }

                    indemnites_data.append({
                        'Indemnité': config_col.title(),
                        'Total': total,
                        'Moyenne': moyenne,
                        'Bénéficiaires': nb_employes,
                        'Pourcentage': pourcentage_beneficiaires,
                        'Color': config['color']
                    })

    # Affichage général
    if stats:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                        padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h2 style="color: #2c3e50; text-align: center; margin-bottom: 20px;">
                     Vue d'ensemble
                </h2>
            </div>
            """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_indemnites = sum([s['Total'] for s in stats.values()])
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 20px; border-radius: 10px; text-align: center;
                            box-shadow: 0 4px 15px rgba(102,126,234,0.2);">
                    <h3 style="color: white; margin: 0;">Total indemnités</h3>
                    <p style="color: white; font-size: 1.8em; margin: 10px 0 0 0;">
                        {total_indemnites:,.0f} DH
                    </p>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            moyenne_globale = sum([s['Moyenne'] for s in stats.values()]) / len(stats)
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
                            padding: 20px; border-radius: 10px; text-align: center;
                            box-shadow: 0 4px 15px rgba(78,205,196,0.2);">
                    <h3 style="color: white; margin: 0;">Moyenne globale</h3>
                    <p style="color: white; font-size: 1.8em; margin: 10px 0 0 0;">
                        {moyenne_globale:,.0f} DH
                    </p>
                </div>
                """, unsafe_allow_html=True)

        with col3:
            total_beneficiaires = sum([s['Nombre des employés concernés'] for s in stats.values()])
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%);
                            padding: 20px; border-radius: 10px; text-align: center;
                            box-shadow: 0 4px 15px rgba(254,202,87,0.2);">
                    <h3 style="color: white; margin: 0;">Total bénéficiaires</h3>
                    <p style="color: white; font-size: 1.8em; margin: 10px 0 0 0;">
                        {total_beneficiaires}
                    </p>
                </div>
                """, unsafe_allow_html=True)

        with col4:
            indemnite_populaire = max(stats.items(), key=lambda x: x[1]['Pourcentage de bénéficiaires'])
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                            padding: 20px; border-radius: 10px; text-align: center;
                            box-shadow: 0 4px 15px rgba(255,107,107,0.2);">
                    <h3 style="color: white; margin: 0;">Plus populaire</h3>
                    <p style="color: white; font-size: 1.2em; margin: 10px 0 0 0;">
                        {indemnite_populaire[0].title()}
                    </p>
                </div>
                """, unsafe_allow_html=True)

        # Graphique camembert
        st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 20px; border-radius: 10px; margin: 30px 0 20px 0;">
                <h2 style="color: white; text-align: center; margin: 0;">
                     📊 Répartition des Indemnités
                </h2>
            </div>
            """, unsafe_allow_html=True)

        # Préparer les données pour le camembert
        import plotly.express as px
        import plotly.graph_objects as go

        if indemnites_data:
            # Créer le DataFrame pour le graphique
            df_pie = pd.DataFrame(indemnites_data)

            # Créer le camembert avec Plotly
            fig = px.pie(
                df_pie,
                values='Total',
                names='Indemnité',
                title="Répartition des Indemnités par Montant Total",
                color_discrete_sequence=[item['Color'] for item in indemnites_data]
            )

            # Personnaliser le graphique
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>' +
                              'Montant: %{value:,.0f} DH<br>' +
                              'Pourcentage: %{percent}<br>' +
                              '<extra></extra>'
            )

            fig.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.01
                ),
                font=dict(size=12),
                margin=dict(l=20, r=20, t=70, b=20),
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

            # Tableau récapitulatif sous le graphique
            st.markdown("""
                <div style="margin-top: 20px;">
                    <h4 style="color: #2c3e50; text-align: center;">📋 Tableau Récapitulatif</h4>
                </div>
                """, unsafe_allow_html=True)



        # Détail par indemnité - Version simplifiée
        st.markdown("""
            <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                        padding: 20px; border-radius: 10px; margin: 30px 0 20px 0;">
                <h2 style="color: #2c3e50; text-align: center; margin: 0;">
                     📋 Détail par indemnité
                </h2>
            </div>
            """, unsafe_allow_html=True)

        for col, stat in stats.items():
            with st.expander(f"🔹 {col.title()}", expanded=True):
                st.markdown(f"""
                    <div style="background: {stat['bg']}; padding: 15px; border-radius: 8px; 
                                border-left: 4px solid {stat['color']};">
                    """, unsafe_allow_html=True)

                # Affichage simplifié avec seulement les 4 statistiques essentielles
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"""
                        **Montants**
                        - Total: **{stat['Total']:,.2f} DH**
                        - Moyenne: **{stat['Moyenne']:,.2f} DH**
                        """)
                with c2:
                    st.markdown(f"""
                        **Bénéficiaires**
                        - Nombre: **{stat['Nombre des employés concernés']}**
                        - Pourcentage: **{stat['Pourcentage de bénéficiaires']:.1f}%**
                        """)

                st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.warning("⚠️ Aucune donnée d'indemnité trouvée dans les colonnes disponibles")
        st.info("Colonnes disponibles : " + ", ".join(df.columns))

    # Téléchargement des statistiques simplifiées
    if stats:
        df_stats = pd.DataFrame(indemnites_data)

        st.markdown("""
            <div style="margin-top:30px; padding:20px; background:linear-gradient(135deg,#667eea 0%,#764ba2 50%);
                        border-radius:10px; text-align:center;">
                <h3 style="color:white; margin:0;">📥 Télécharger les statistiques</h3>
            </div>
            """, unsafe_allow_html=True)
        # 🚗 Section des employés avec voiture de fonction (TOUJOURS AFFICHÉE)
        st.markdown("""
               <div style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
                           padding: 20px; border-radius: 10px; margin: 30px 0 20px 0;">
                   <h2 style="color: #2c3e50; text-align: center; margin: 0;">
                       Employés avec voiture de fonction
                   </h2>
               </div>
               """, unsafe_allow_html=True)

        # Rechercher la colonne voiture
        voiture_col = None
        for col in df.columns:
            if 'voiture' in col.lower():
                voiture_col = col
                break

        # Initialiser les DataFrames pour l'export
        df_voitures_display = pd.DataFrame()
        repartition_voitures = pd.DataFrame()

        if voiture_col is not None:
            # Filtrer les employés qui ont une voiture (valeur non vide et non NaN)
            df_voitures = df[df[voiture_col].notna() & (df[voiture_col] != '') & (
                    df[voiture_col].astype(str).str.strip() != '')].copy()

            if not df_voitures.empty:
                # Créer un tableau des employés avec voiture
                colonnes_importantes = []

                # Chercher les colonnes importantes (nom, prénom, etc.)
                for col in df.columns:
                    col_lower = col.lower()
                    if any(keyword in col_lower for keyword in ['nom', 'prénom', 'prenom', 'name', 'matricule', 'id']):
                        colonnes_importantes.append(col)

                # Ajouter la colonne voiture
                colonnes_importantes.append(voiture_col)

                # Créer le DataFrame des voitures
                df_voitures_display = df_voitures[colonnes_importantes].copy()
                df_voitures_display = df_voitures_display.reset_index(drop=True)

                # Statistiques des voitures
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(f"""
                           <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                       padding: 20px; border-radius: 10px; text-align: center;
                                       box-shadow: 0 4px 15px rgba(102,126,234,0.2);">
                               <h3 style="color: white; margin: 0;">Total employés</h3>
                               <p style="color: white; font-size: 1.8em; margin: 10px 0 0 0;">
                                   {len(df_voitures_display)}
                               </p>
                           </div>
                           """, unsafe_allow_html=True)

                with col2:
                    pourcentage_voitures = (len(df_voitures_display) / len(df)) * 100 if len(df) > 0 else 0
                    st.markdown(f"""
                           <div style="background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
                                       padding: 20px; border-radius: 10px; text-align: center;
                                       box-shadow: 0 4px 15px rgba(78,205,196,0.2);">
                               <h3 style="color: white; margin: 0;">Pourcentage</h3>
                               <p style="color: white; font-size: 1.8em; margin: 10px 0 0 0;">
                                   {pourcentage_voitures:.1f}%
                               </p>
                           </div>
                           """, unsafe_allow_html=True)

                with col3:
                    # Compter les types de voitures uniques
                    types_voitures = df_voitures[voiture_col].nunique()
                    st.markdown(f"""
                           <div style="background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%);
                                       padding: 20px; border-radius: 10px; text-align: center;
                                       box-shadow: 0 4px 15px rgba(254,202,87,0.2);">
                               <h3 style="color: white; margin: 0;">Types de voitures</h3>
                               <p style="color: white; font-size: 1.8em; margin: 10px 0 0 0;">
                                   {types_voitures}
                               </p>
                           </div>
                           """, unsafe_allow_html=True)

                # Afficher le tableau
                st.markdown("""
                       <div style="margin: 20px 0;">
                           <h3 style="color: #2c3e50;">📋 Liste des employés avec voiture</h3>
                       </div>
                       """, unsafe_allow_html=True)

                st.dataframe(
                    df_voitures_display,
                    use_container_width=True,
                    hide_index=True
                )

                # Répartition par type de voiture
                st.markdown("""
                       <div style="margin: 20px 0;">
                           <h3 style="color: #2c3e50;">Répartition par type de voiture</h3>
                       </div>
                       """, unsafe_allow_html=True)

                repartition_voitures = df_voitures[voiture_col].value_counts().reset_index()
                repartition_voitures.columns = ['Type de voiture', 'Nombre d\'employés']

                st.dataframe(
                    repartition_voitures,
                    use_container_width=True,
                    hide_index=True
                )

            else:
                st.info("ℹ️ Aucun employé n'a de voiture de fonction attribuée.")
        else:
            st.warning("⚠️ Colonne 'voiture' non trouvée dans les données.")
            st.info("📋 Colonnes disponibles : " + ", ".join(df.columns))

        # Si aucune donnée d'indemnité n'est trouvée
        if not stats:
            st.warning("⚠️ Aucune donnée d'indemnité trouvée dans les colonnes disponibles")
            st.info("📋 Colonnes disponibles : " + ", ".join(df.columns))

        # ➡️ Téléchargement Excel avec toutes les données
        df_stats = pd.DataFrame(indemnites_data) if indemnites_data else pd.DataFrame()

        st.markdown("""
               <div style="margin-top:30px; padding:20px; background:linear-gradient(135deg,#667eea 0%,#764ba2 50%);
                           border-radius:10px; text-align:center;">
                   <h3 style="color:white; margin:0;">📥 Télécharger les statistiques</h3>
               </div>
               """, unsafe_allow_html=True)

        import io

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Feuille des données brutes
            df.to_excel(writer, sheet_name='Données brutes', index=False)

            # Feuille des statistiques détaillées
            df_stats_excel = df_stats.copy()
            df_stats_excel.to_excel(writer, sheet_name='Statistiques détaillées', index=False)

            # Feuille spéciale pour le camembert
            df_camembert = pd.DataFrame({
                'Indemnité': [item['Indemnité'] for item in indemnites_data],
                'Montant Total (DH)': [item['Total'] for item in indemnites_data],
                'Pourcentage du Total (%)': [(item['Total'] / sum([i['Total'] for i in indemnites_data]) * 100) for item
                                             in indemnites_data]
            })
            df_camembert.to_excel(writer, sheet_name='Données Camembert', index=False)
            # Employés avec voiture (si disponibles)
            if not df_voitures_display.empty:
                df_voitures_display.to_excel(writer, sheet_name='Employés avec voiture', index=False)

            # Répartition des voitures (si disponibles)
            if not repartition_voitures.empty:
                repartition_voitures.to_excel(writer, sheet_name='Répartition voitures', index=False)

        output.seek(0)

        st.download_button(
            "📥 Télécharger le fichier Excel complet",
            data=output,
            file_name="indemnites_rapport.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
