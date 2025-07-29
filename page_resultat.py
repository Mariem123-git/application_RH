from utils import recherche_employe


def run(df):
    import streamlit as st
    import io
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    st.header("📑 Résultat Final & Paiement")
    df_filtered = recherche_employe(df)
    # Option : utiliser le DataFrame filtré ou non
    use_filtered = st.checkbox("📊 Utiliser le filtre pour les graphiques", value=False)
    if use_filtered:
        df = df_filtered

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

             .stat-label {
                 font-weight: 600;
             }

             .stat-number {
                 font-weight: bold;
                 font-size: 20px;
             }
         </style>
         """, unsafe_allow_html=True)

    # ✅ Nettoyage des noms de colonnes
    df.columns = [col.strip() for col in df.columns]

    # ✅ Statistiques par type de salaire
    stats = {}
    cols_with_titles = {
        'Salaire brut': 'Salaire brut',
        'salaire net': 'salaire net',
        'Salaire net à payer': 'Salaire net à payer'
    }

    colors = {
        'Salaire brut': "salary-card-blue",
        'salaire net': "salary-card-green",
        'Salaire net à payer': "salary-card-orange"
    }

    for col, titre in cols_with_titles.items():
        if col in df.columns:
            serie_num = pd.to_numeric(df[col], errors='coerce')
            total = serie_num.sum()
            moyenne = serie_num.mean()
            maximum = serie_num.max()
            minimum = serie_num.min()
            median = serie_num.median()

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

    # ✅ Tableau des salaires < 3000 DH
    if 'Salaire net à payer' in df.columns:
        salaire_data = pd.to_numeric(df['Salaire net à payer'], errors='coerce')
        df_faibles_salaires = df[salaire_data < 3000].copy()

        if not df_faibles_salaires.empty:
            st.subheader("⚠️ Employés avec salaire net < 3000 DH (SMIC)")
            cols_affichage = ['Noms & Prénoms', 'Salaire brut', 'salaire net', 'Salaire net à payer']
            cols_existants = [c for c in cols_affichage if c in df_faibles_salaires.columns]
            st.dataframe(df_faibles_salaires[cols_existants], use_container_width=True, height=300)

            st.warning(f"⚠️ {len(df_faibles_salaires)} employé(s) ont un salaire net inférieur au SMIC (3000 DH)")

    # ✅ Liste des salariés concernés par avances et prêts
    cols_affichage = ['Noms & Prénoms', 'Salaire brut', 'salaire net', 'Avance s/salaire', 'Rbst Prêt',
                      'Salaire net à payer']
    cols_existants = [c for c in cols_affichage if c in df.columns]

    # Initialiser les DataFrames vides
    df_avances = pd.DataFrame()
    df_prets = pd.DataFrame()

    if 'Avance s/salaire' in df.columns:
        df_avances = df[pd.to_numeric(df['Avance s/salaire'], errors='coerce') > 0]
        if not df_avances.empty:
            st.subheader("📄 Liste employés avec avances")
            st.dataframe(df_avances[cols_existants], use_container_width=True, height=400)

    if 'Rbst Prêt' in df.columns:
        df_prets = df[pd.to_numeric(df['Rbst Prêt'], errors='coerce') > 0]
        if not df_prets.empty:
            st.subheader("📄 Liste employés avec prêts")
            st.dataframe(df_prets[cols_existants], use_container_width=True, height=400)

    # ========== SECTION GRAPHIQUES ==========
    st.header("📊 Graphiques d'Analyse")

    # Configuration matplotlib pour une meilleure lisibilité
    plt.rcParams.update({
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'axes.edgecolor': 'black',
        'axes.linewidth': 1,
        'xtick.color': 'black',
        'ytick.color': 'black',
        'text.color': 'black',
        'font.size': 12,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10
    })

    # === 1. GRAPHIQUE DES AVANCES ===
    img_avances = io.BytesIO()
    if 'Avance s/salaire' in df.columns:
        avances_data = pd.to_numeric(df['Avance s/salaire'], errors='coerce').dropna()
        avances_data = avances_data[avances_data > 0]

        if not avances_data.empty:
            fig_avances, ax_avances = plt.subplots(figsize=(10, 8))

            # Créer des tranches logiques
            tranches = ['0-500 DH', '500-1000 DH', '1000-2000 DH', '2000+ DH']
            counts = [
                len(avances_data[(avances_data > 0) & (avances_data <= 500)]),
                len(avances_data[(avances_data > 500) & (avances_data <= 1000)]),
                len(avances_data[(avances_data > 1000) & (avances_data <= 2000)]),
                len(avances_data[avances_data > 2000])
            ]

            # Filtrer les tranches non vides
            tranches_filtered = [t for t, c in zip(tranches, counts) if c > 0]
            counts_filtered = [c for c in counts if c > 0]

            if counts_filtered:
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'][:len(counts_filtered)]

                wedges, texts, autotexts = ax_avances.pie(
                    counts_filtered,
                    labels=tranches_filtered,
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=colors,
                    textprops={'fontsize': 11, 'weight': 'bold'}
                )

                ax_avances.set_title(
                    f'Répartition des Avances sur Salaire\n'
                    f'Total: {avances_data.sum():,.0f} DH | '
                    f'Employés concernés: {len(avances_data)} | '
                    f'Moyenne: {avances_data.mean():,.0f} DH',
                    fontsize=14, weight='bold', pad=20
                )

                st.subheader("📊 Répartition des Avances")
                st.pyplot(fig_avances)
                fig_avances.savefig(img_avances, format='png', dpi=300, bbox_inches='tight')
                plt.close(fig_avances)

    # === 2. GRAPHIQUE DES PRÊTS ===
    img_prets = io.BytesIO()
    if 'Rbst Prêt' in df.columns:
        prets_data = pd.to_numeric(df['Rbst Prêt'], errors='coerce').dropna()
        prets_data = prets_data[prets_data > 0]

        if not prets_data.empty:
            fig_prets, ax_prets = plt.subplots(figsize=(10, 8))

            # Créer des tranches pour les prêts
            tranches_prets = ['0-1000 DH', '1000-3000 DH', '3000-5000 DH', '5000+ DH']
            counts_prets = [
                len(prets_data[(prets_data > 0) & (prets_data <= 1000)]),
                len(prets_data[(prets_data > 1000) & (prets_data <= 3000)]),
                len(prets_data[(prets_data > 3000) & (prets_data <= 5000)]),
                len(prets_data[prets_data > 5000])
            ]

            # Filtrer les tranches non vides
            tranches_prets_filtered = [t for t, c in zip(tranches_prets, counts_prets) if c > 0]
            counts_prets_filtered = [c for c in counts_prets if c > 0]

            if counts_prets_filtered:
                colors_prets = ['#FFB74D', '#81C784', '#64B5F6', '#F06292'][:len(counts_prets_filtered)]

                wedges, texts, autotexts = ax_prets.pie(
                    counts_prets_filtered,
                    labels=tranches_prets_filtered,
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=colors_prets,
                    textprops={'fontsize': 11, 'weight': 'bold'}
                )

                ax_prets.set_title(
                    f'Répartition des Remboursements de Prêts\n'
                    f'Total: {prets_data.sum():,.0f} DH | '
                    f'Employés concernés: {len(prets_data)} | '
                    f'Moyenne: {prets_data.mean():,.0f} DH',
                    fontsize=14, weight='bold', pad=20
                )

                st.subheader("📊 Répartition des Prêts")
                st.pyplot(fig_prets)
                fig_prets.savefig(img_prets, format='png', dpi=300, bbox_inches='tight')
                plt.close(fig_prets)

    # === 3. HISTOGRAMME SALAIRE NET À PAYER EN FONCTION DE L'EFFECTIF ===
    img_hist_net = io.BytesIO()
    if 'Salaire net à payer' in df.columns:
        salaire_net_data = pd.to_numeric(df['Salaire net à payer'], errors='coerce').dropna()
        salaire_net_data = salaire_net_data[salaire_net_data > 0]

        if not salaire_net_data.empty:
            fig_hist_net, ax_hist_net = plt.subplots(figsize=(14, 8))

            # Créer des bins optimisés
            n_bins = min(20, len(salaire_net_data.unique()))

            n, bins, patches = ax_hist_net.hist(
                salaire_net_data,
                bins=n_bins,
                color='#E74C3C',
                edgecolor='black',
                alpha=0.7,
                linewidth=1
            )

            # Ajouter les nombres d'effectifs à l'intérieur des barres
            for i, (count, patch) in enumerate(zip(n, patches)):
                if count > 0:  # Afficher seulement si la barre n'est pas vide
                    # Position du texte au centre de la barre
                    x_pos = (bins[i] + bins[i + 1]) / 2
                    y_pos = count / 2

                    ax_hist_net.text(x_pos, y_pos, f'{int(count)}',
                                     ha='center', va='center',
                                     fontsize=10, fontweight='bold',
                                     color='white',
                                     bbox=dict(boxstyle='round,pad=0.2',
                                               facecolor='black', alpha=0.7))

            # Lignes de référence
            ax_hist_net.axvline(x=3000, color='red', linestyle='--', linewidth=3,
                                label='SMIC (3000 DH)', alpha=0.8)
            ax_hist_net.axvline(x=salaire_net_data.mean(), color='orange', linestyle='-', linewidth=3,
                                label=f'Moyenne: {salaire_net_data.mean():.0f} DH', alpha=0.8)
            ax_hist_net.axvline(x=salaire_net_data.median(), color='green', linestyle=':', linewidth=3,
                                label=f'Médiane: {salaire_net_data.median():.0f} DH', alpha=0.8)

            ax_hist_net.set_title('Distribution des Salaires Net à Payer par Effectif',
                                  fontsize=16, weight='bold', pad=20)
            ax_hist_net.set_xlabel('Salaire Net à Payer (DH)', fontsize=14, weight='bold')
            ax_hist_net.set_ylabel('Nombre d\'Employés (Effectif)', fontsize=14, weight='bold')
            ax_hist_net.legend(fontsize=12)
            ax_hist_net.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

            # Statistiques dans un encadré
            stats_text = (
                          f'Min: {salaire_net_data.min():,.0f} DH\n'
                          f'Max: {salaire_net_data.max():,.0f} DH\n'
                          f'Écart-type: {salaire_net_data.std():,.0f} DH')

            props = dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8)
            ax_hist_net.text(0.72, 0.98, stats_text, transform=ax_hist_net.transAxes,
                             fontsize=11, verticalalignment='top', bbox=props)

            st.subheader("📊 Distribution des Salaires Net à Payer")
            st.pyplot(fig_hist_net)
            fig_hist_net.savefig(img_hist_net, format='png', dpi=300, bbox_inches='tight')
            plt.close(fig_hist_net)

    # === 4. HISTOGRAMME SALAIRE BRUT EN FONCTION DE L'EFFECTIF ===
    img_hist_brut = io.BytesIO()
    if 'Salaire brut' in df.columns:
        salaire_brut_data = pd.to_numeric(df['Salaire brut'], errors='coerce').dropna()
        salaire_brut_data = salaire_brut_data[salaire_brut_data > 0]

        if not salaire_brut_data.empty:
            fig_hist_brut, ax_hist_brut = plt.subplots(figsize=(14, 8))

            # Créer des bins optimisés
            n_bins = min(20, len(salaire_brut_data.unique()))

            n, bins, patches = ax_hist_brut.hist(
                salaire_brut_data,
                bins=n_bins,
                color='#3498DB',
                edgecolor='black',
                alpha=0.7,
                linewidth=1
            )

            # Ajouter les nombres d'effectifs à l'intérieur des barres
            for i, (count, patch) in enumerate(zip(n, patches)):
                if count > 0:  # Afficher seulement si la barre n'est pas vide
                    # Position du texte au centre de la barre
                    x_pos = (bins[i] + bins[i + 1]) / 2
                    y_pos = count / 2

                    ax_hist_brut.text(x_pos, y_pos, f'{int(count)}',
                                      ha='center', va='center',
                                      fontsize=10, fontweight='bold',
                                      color='white',
                                      bbox=dict(boxstyle='round,pad=0.2',
                                                facecolor='black', alpha=0.7))

            # Lignes de référence
            ax_hist_brut.axvline(x=salaire_brut_data.mean(), color='orange', linestyle='-', linewidth=3,
                                 label=f'Moyenne: {salaire_brut_data.mean():.0f} DH', alpha=0.8)
            ax_hist_brut.axvline(x=salaire_brut_data.median(), color='green', linestyle=':', linewidth=3,
                                 label=f'Médiane: {salaire_brut_data.median():.0f} DH', alpha=0.8)

            ax_hist_brut.set_title('Distribution des Salaires Brut par Effectif',
                                   fontsize=16, weight='bold', pad=20)
            ax_hist_brut.set_xlabel('Salaire Brut (DH)', fontsize=14, weight='bold')
            ax_hist_brut.set_ylabel('Nombre d\'Employés (Effectif)', fontsize=14, weight='bold')
            ax_hist_brut.legend(fontsize=12)
            ax_hist_brut.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

            # Statistiques dans un encadré
            stats_text = (
                          f'Min: {salaire_brut_data.min():,.0f} DH\n'
                          f'Max: {salaire_brut_data.max():,.0f} DH\n'
                          f'Écart-type: {salaire_brut_data.std():,.0f} DH')

            props = dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.8)
            ax_hist_brut.text(0.72, 0.98, stats_text, transform=ax_hist_brut.transAxes,
                              fontsize=11, verticalalignment='top', bbox=props)

            st.subheader("📊 Distribution des Salaires Brut")
            st.pyplot(fig_hist_brut)
            fig_hist_brut.savefig(img_hist_brut, format='png', dpi=300, bbox_inches='tight')
            plt.close(fig_hist_brut)

    # ✅ Générer le Excel avec plusieurs feuilles
    df_stats = pd.DataFrame([stats])
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_stats.to_excel(writer, sheet_name='Statistiques', index=False)

        if not df_avances.empty:
            df_avances.to_excel(writer, sheet_name='Avances', index=False)

        if not df_prets.empty:
            df_prets.to_excel(writer, sheet_name='Prets', index=False)

        # Ajouter le tableau des faibles salaires s'il existe
        if 'df_faibles_salaires' in locals() and not df_faibles_salaires.empty:
            df_faibles_salaires.to_excel(writer, sheet_name='Salaires_Inferieurs_SMIC', index=False)

        workbook = writer.book
        worksheet = workbook.add_worksheet('Graphiques')
        writer.sheets['Graphiques'] = worksheet

        # Insérer les graphiques dans Excel
        row_position = 2
        if 'img_avances' in locals() and img_avances.getvalue():
            worksheet.insert_image(f'B{row_position}', 'avances.png', {'image_data': img_avances})
            row_position += 30

        if 'img_prets' in locals() and img_prets.getvalue():
            worksheet.insert_image(f'B{row_position}', 'prets.png', {'image_data': img_prets})
            row_position += 30

        if 'img_hist_net' in locals() and img_hist_net.getvalue():
            worksheet.insert_image(f'B{row_position}', 'hist_salaire_net.png', {'image_data': img_hist_net})
            row_position += 30

        if 'img_hist_brut' in locals() and img_hist_brut.getvalue():
            worksheet.insert_image(f'B{row_position}', 'hist_salaire_brut.png', {'image_data': img_hist_brut})

    output.seek(0)

    # === ✅ BOUTON DE TÉLÉCHARGEMENT ===
    st.download_button(
        "📥 Télécharger le fichier Excel complet",
        data=output,
        file_name="rapport_salaire_complet.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
