import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Tableau de bord Brevets", layout="wide")

# Titre
st.title("📊 Tableau de bord")

# Menu latéral
st.sidebar.header("Filtres")
st.sidebar.text("Sélectionnez vos critères")

st.write("Bienvenue sur le tableau de bord des brevets !")


import pandas as pd

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

# Charger les données
@st.cache_data
def load_data():
    return pd.read_csv("brevets_6G.csv")

df = load_data()
st.write("Aperçu des brevets :", df.head(10))


from st_aggrid import AgGrid

st.subheader("Données des brevets")
AgGrid(df, editable=True, height=400)

# Comptage des brevets
total_brevets = len(df)
brevets_traités = df[df['Status'] == 'Traité'].shape[0]  # Supposons qu'on ait une colonne 'Statut'
brevets_restants = total_brevets - brevets_traités

# Nombre de brevets en cours
brevets_en_cours = df[df["Status"] == "En cours"].shape[0]



# Progression du traitement
progress = brevets_traités / total_brevets if total_brevets > 0 else 0

st.progress(progress)
st.write(f"🔵 {brevets_traités} sur {total_brevets} brevets traités ({progress * 100:.2f}%)")


from st_aggrid import GridOptionsBuilder, AgGrid

st.subheader("✏️ Modifier les brevets")

# Options de configuration
grid_options = GridOptionsBuilder.from_dataframe(df)
grid_options.configure_default_column(editable=True)  # Rend toutes les colonnes éditables
grid_options.configure_pagination()  # Ajoute une pagination
grid_options.configure_side_bar()  # Ajoute une barre latérale

# Affichage du tableau éditable
grid_response = AgGrid(df, gridOptions=grid_options.build(), editable=True, height=400)

# Récupération des nouvelles données
df_modifié = grid_response["data"]

import io

st.subheader("💾 Télécharger les données mises à jour")

# Sauvegarde du fichier modifié
buffer = io.BytesIO()
df_modifié.to_excel(buffer, index=False, engine='openpyxl')
buffer.seek(0)

st.download_button(label="📥 Télécharger le fichier Excel",
                   data=buffer,
                   file_name="brevets_mis_a_jour.xlsx",
                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
