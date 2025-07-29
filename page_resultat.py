
from utils import recherche_employe

def run(df):
    import streamlit as st
    import io

    st.header("📑 Résultat Final & Paiement")
    df_filtered = recherche_employe(df)
    # Option : utiliser le DataFrame filtré ou non
    use_filtered = st.checkbox("📊 Utiliser le filtre pour les graphiques", value=False)
    if use_filtered:
        df = df_filtered  # ✅ Pas de deux-points ici !

    df = df.iloc[:-1, :]



    # CSS pour le style des cartes
    st.markdown("""
         <style>
             .salary-card {
                 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                 padding: 20px;
                 border-radius: 15px;
                 margin: 10px 0;
                 box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                 color: white;
                 border: 1px solid rgba(255,255,255,0.2);
             }

             .salary-card-green {
                 background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
                 padding: 20px;
                 border-radius: 15px;
                 margin: 10px 0;
                 box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                 color: white;
                 border: 1px solid rgba(255,255,255,0.2);
             }

             .salary-card-orange {
                 background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                 padding: 20px;
                 border-radius: 15px;
                 margin: 10px 0;
                 box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                 color: white;
                 border: 1px solid rgba(255,255,255,0.2);
             }

             .salary-card-blue {
                 background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                 padding: 20px;
                 border-radius: 15px;
                 margin: 10px 0;
                 box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                 color: white;
                 border: 1px solid rgba(255,255,255,0.2);
             }

             .salary-card-purple {
                 background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                 padding: 20px;
                 border-radius: 15px;
                 margin: 10px 0;
                 box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                 color: #333;
                 border: 1px solid rgba(255,255,255,0.2);
             }

             .stat-title {
                 font-size: 24px;
                 font-weight: bold;
                 margin-bottom: 15px;
                 text-align: center;
                 text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
             }

             .stat-value {
                 font-size: 18px;
                 margin: 8px 0;
                 display: flex;
                 justify-content: space-between;
                 align-items: center;
             }

             .stat-label {
                 font-weight: 600;
             }

             .stat-number {
                 font-weight: bold;
                 font-size: 20px;
             }

             .summary-card {
                 background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
                 padding: 25px;
                 border-radius: 20px;
                 margin: 20px 0;
                 box-shadow: 0 12px 40px rgba(0,0,0,0.15);
                 color: #333;
                 border: 2px solid rgba(255,255,255,0.3);
             }

             .metric-container {
                 display: flex;
                 justify-content: space-around;
                 flex-wrap: wrap;
                 margin: 20px 0;
             }

             .metric-box {
                 background: rgba(255,255,255,0.2);
                 padding: 15px;
                 border-radius: 10px;
                 margin: 5px;
                 min-width: 150px;
                 text-align: center;
                 backdrop-filter: blur(10px);
             }

             .alert-card {
                 background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                 padding: 20px;
                 border-radius: 15px;
                 margin: 15px 0;
                 color: #333;
                 border: 1px solid rgba(255,255,255,0.2);
                 box-shadow: 0 8px 32px rgba(0,0,0,0.1);
             }
         </style>
         """, unsafe_allow_html=True)

    # Fonction pour créer des statistiques stylées
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    import seaborn as sns
    import matplotlib.pyplot as plt

    def create_salary_statistics(df):
        # ✅ Nettoyage des noms de colonnes
        df.columns = [col.strip() for col in df.columns]

        st.markdown('<div class="summary-card">', unsafe_allow_html=True)
        st.markdown('<div class="stat-title"> STATISTIQUES DES SALAIRES</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        stats = {}

        cols_with_titles = {
            'Salaire brut': 'Salaire brut',
            'salaire net': 'salaire net',
            'Salaire net à payer': 'Salaire net à payer'
        }

        # Couleurs CSS pour chaque carte
        colors = {
            'Salaire brut': "salary-card-blue",
            'salaire net': "salary-card-green",
            'Salaire net à payer': "salary-card-orange"
        }

        # ✅ Boucle sur les colonnes de salaire
        for col, titre in cols_with_titles.items():
            if col in df.columns:
                serie_num = pd.to_numeric(df[col], errors='coerce')
                total = serie_num.sum()
                moyenne = serie_num.mean()
                maximum = serie_num.max()
                minimum = serie_num.min()
                median = serie_num.median()

                # Carte stylisée
                st.markdown(f'''
                     <div class="{colors[col]}">
                         <h3 style="margin-bottom:10px;">{titre}</h3>
                         <div class="metric-container">
                             <div class="metric-box">
                                 <div class="stat-label">Total</div>
                                 <div class="stat-number">{total:,.0f} DH</div>
                             </div>
                             <div class="metric-box">
                                 <div class="stat-label">Moyenne</div>
                                 <div class="stat-number">{moyenne:,.0f} DH</div>
                             </div>
                             <div class="metric-box">
                                 <div class="stat-label">Médiane</div>
                                 <div class="stat-number">{median:,.0f} DH</div>
                             </div>
                             <div class="metric-box">
                                 <div class="stat-label">Maximum</div>
                                 <div class="stat-number">{maximum:,.0f} DH</div>
                             </div>
                             <div class="metric-box">
                                 <div class="stat-label">Minimum</div>
                                 <div class="stat-number">{minimum:,.0f} DH</div>
                             </div>
                         </div>
                     </div>
                     ''', unsafe_allow_html=True)

                stats[f'{col}_total'] = total
                stats[f'{col}_moyenne'] = moyenne

        # ✅ Avances et prêts
        col1, col2 = st.columns(2)

        with col1:
            if 'Avance s/salaire' in df.columns:
                avance_series = pd.to_numeric(df['Avance s/salaire'], errors='coerce')
                nb_avance = (avance_series > 0).sum()
                total_avance = avance_series.sum()

                st.markdown(f'''
                     <div class="salary-card-purple">
                         <div class="stat-title"> Avances sur Salaire</div>
                         <div class="metric-container">
                             <div class="metric-box">
                                 <div class="stat-label">Employés concernés</div>
                                 <div class="stat-number">{nb_avance}</div>
                             </div>
                             <div class="metric-box">
                                 <div class="stat-label">Montant total</div>
                                 <div class="stat-number">{total_avance:,.0f} DH</div>
                             </div>
                         </div>
                     </div>
                     ''', unsafe_allow_html=True)

        with col2:
            if 'Rbst Prêt' in df.columns:
                pret_series = pd.to_numeric(df['Rbst Prêt'], errors='coerce')
                nb_pret = (pret_series > 0).sum()
                total_pret = pret_series.sum()

                st.markdown(f'''
                     <div class="salary-card">
                         <div class="stat-title"> Remboursements Prêts</div>
                         <div class="metric-container">
                             <div class="metric-box">
                                 <div class="stat-label">Employés concernés</div>
                                 <div class="stat-number">{nb_pret}</div>
                             </div>
                             <div class="metric-box">
                                 <div class="stat-label">Montant total</div>
                                 <div class="stat-number">{total_pret:,.0f} DH</div>
                             </div>
                         </div>
                     </div>
                     ''', unsafe_allow_html=True)

        return stats

    # ✅ Appel de la fonction
    stats = create_salary_statistics(df)

    # ✅ Liste des salariés concernés
    cols_affichage = ['Matricule', 'Noms & Prénoms', 'Salaire brut', 'salaire net', 'Avance s/salaire', 'Rbst Prêt']
    cols_existants = [c for c in cols_affichage if c in df.columns]

    if 'Avance s/salaire' in df.columns:
        df_avances = df[df['Avance s/salaire'] > 0]
        if not df_avances.empty:
            st.subheader("📄 Liste employés avec avances")
            st.dataframe(df_avances[cols_existants], use_container_width=True, height=400)

    if 'Rbst Prêt' in df.columns:
        df_prets = df[df['Rbst Prêt'] > 0]
        if not df_prets.empty:
            st.subheader("📄 Liste employés avec prêts")
            st.dataframe(df_prets[cols_existants], use_container_width=True, height=400)

    # ✅ Graphe 1 : Camembert Avances / Prêts
    labels = []
    values = []

    if 'Avance s/salaire' in df.columns:
        total_avance = pd.to_numeric(df['Avance s/salaire'], errors='coerce').sum()
        if total_avance > 0:
            labels.append("Avances sur salaire")
            values.append(total_avance)

    if 'Rbst Prêt' in df.columns:
        total_pret = pd.to_numeric(df['Rbst Prêt'], errors='coerce').sum()
        if total_pret > 0:
            labels.append("Remboursements Prêts")
            values.append(total_pret)

    df_stats = pd.DataFrame([stats])
    df_stats = pd.DataFrame([stats])  # ✅ Corrigé

    # 🟢 -- Sauvegarder le camembert --
    img_camembert = io.BytesIO()
    if values:
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        ax.axis('equal')
        ax.set_title("Répartition Avances & Prêts")
        st.pyplot(fig)
        fig.savefig(img_camembert, format='png')
        img_camembert.seek(0)
    import numpy as np
    # 🟢 -- Sauvegarder l’histogramme --
    img_hist = io.BytesIO()
    if 'salaire net' in df.columns:
        sal_net_series = pd.to_numeric(df['salaire net'], errors='coerce').dropna()
        sal_net_series = sal_net_series[sal_net_series >= 3000]

        if not sal_net_series.empty:
            nbins = 15
            hist_data, bin_edges = np.histogram(sal_net_series, bins=nbins)
            fig_hist, ax_hist = plt.subplots()
            ax_hist.hist(sal_net_series, bins=nbins, color='#4facfe', edgecolor='black')
            ax_hist.set_title('Distribution des Salaires Nets ≥ 3000 DH')
            ax_hist.set_xlabel('Salaire Net (DH)')
            ax_hist.set_ylabel('Effectif')
            st.pyplot(fig_hist)
            fig_hist.savefig(img_hist, format='png')
            img_hist.seek(0)

    # ✅ Générer le Excel avec plusieurs feuilles
    # -----------------------------
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:

        df_stats.to_excel(writer, sheet_name='Statistiques', index=False)


        if not df_avances.empty:
            df_avances.to_excel(writer, sheet_name='Avances', index=False)


        if not df_prets.empty:
            df_prets.to_excel(writer, sheet_name='Prets', index=False)


        workbook = writer.book
        worksheet = workbook.add_worksheet('Graphiques')
        writer.sheets['Graphiques'] = worksheet

        # Insérer camembert SI NON VIDE
        if values:
            worksheet.insert_image('B2', 'camembert.png', {'image_data': img_camembert})

        # Insérer histogramme SI NON VIDE
        if 'salaire net' in df.columns and not sal_net_series.empty:
            worksheet.insert_image('B25', 'histogramme.png', {'image_data': img_hist})

    output.seek(0)

    # === ✅ BOUTON DE TÉLÉCHARGEMENT ===
    st.download_button(
        "📥 Télécharger le fichier Excel complet",
        data=output,
        file_name="rapport_salaire_complet.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )




