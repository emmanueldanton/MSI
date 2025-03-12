import streamlit as st
import pandas as pd
import io
from st_aggrid import AgGrid, GridOptionsBuilder

# Configuration de la page
st.set_page_config(page_title="Tableau de bord Brevets", layout="wide")

# Titre
st.title("📊 Tableau de bord")

# Menu latéral
st.sidebar.header("Filtres")
st.sidebar.text("Sélectionnez vos critères")

st.write("Bienvenue sur le tableau de bord des brevets !")

# Charger les données
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("brevets_6G.csv")
        return df
    except FileNotFoundError:
        st.error("❌ Erreur : Le fichier 'brevets_6G.csv' est introuvable.")
        return pd.DataFrame()  # Retourne un DataFrame vide pour éviter les erreurs

df = load_data()

if not df.empty:
    # Comptage des brevets
    total_brevets = len(df)
    brevets_traités = df[df['Status'] == 'Traité'].shape[0]  # Supposons qu'on ait une colonne 'Status'
    brevets_restants = total_brevets - brevets_traités
    brevets_en_cours = df[df["Status"] == "En cours"].shape[0]

    # Affichage des indicateurs
    col1, col2, col3 = st.columns(3)
    col1.metric(label="📜 Total Brevets", value=total_brevets)
    col2.metric(label="✅ Brevets Traités", value=brevets_traités)
    col3.metric(label="⏳ Brevets Restants", value=brevets_restants)

    # Affichage dynamique
    st.subheader("📡 Suivi des traitements en temps réel")
    col1, col2 = st.columns(2)
    col1.metric("🔄 Brevets en cours", brevets_en_cours)
    col2.metric("✅ Brevets terminés", brevets_traités)

    # Affichage des données
    st.write("Aperçu des brevets :", df.head(10))

    # Affichage d'un tableau interactif
    st.subheader("Données des brevets")
    AgGrid(df, editable=True, height=400)

    # Progression du traitement
    progress = brevets_traités / total_brevets if total_brevets > 0 else 0
    st.progress(progress)
    st.write(f"🔵 {brevets_traités} sur {total_brevets} brevets traités ({progress * 100:.2f}%)")

    # Tableau éditable
    st.subheader("✏️ Modifier les brevets")

    grid_options = GridOptionsBuilder.from_dataframe(df)
    grid_options.configure_default_column(editable=True)
    grid_options.configure_pagination()
    grid_options.configure_side_bar()

    grid_response = AgGrid(df, gridOptions=grid_options.build(), editable=True, height=400)
    df_modifié = grid_response.data

    # Téléchargement des données mises à jour
    st.subheader("💾 Télécharger les données mises à jour")
    buffer = io.BytesIO()
    df_modifié.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)

    st.download_button(
        label="📥 Télécharger le fichier Excel",
        data=buffer,
        file_name="brevets_mis_a_jour.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.warning("⚠️ Aucune donnée disponible pour afficher le tableau de bord.")
