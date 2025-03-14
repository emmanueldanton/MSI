import streamlit as st
import pandas as pd
import plotly.express as px
import wordcloud
import matplotlib.pyplot as plt
#YANN
# 📌 Charger le fichier CSV des brevets
csv_file_path = "brevets_6Gfinal2.csv"
try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    st.error("❌ Le fichier brevets_6Gfinal2.csv est introuvable. Vérifie le chemin.")
    st.stop()

# 📌 Configuration de la page Streamlit
st.set_page_config(page_title="📊 Datavisualisation des brevets 6G", layout="wide")
st.title("📊 Datavisualisation des brevets 6G")

# 🔍 **Section : Indicateurs Clés**
st.subheader("📌 Tableau de bord général")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("📄 Total des brevets recensés", len(df))
with col2:
    st.metric("✅ Brevets traités", len(df))

# 🎯 **Compteurs par statut du brevet**
if "Statut du brevet" in df.columns:
    statut_lower = df["Statut du brevet"].str.lower()

    # Filtrer les brevets actifs (sans expiration indiquée)
    nb_active = df[statut_lower == "active"].shape[0]

    # Filtrer les brevets actifs avec une date d'expiration
    nb_active_exp = df[statut_lower.str.startswith("active, expires", na=False)].shape[0]

    # Filtrer les brevets expirés
    nb_expired = df[statut_lower.str.startswith("expired", na=False)].shape[0]

    with col3:
        st.metric("📗 Brevets actifs", nb_active)
    with col4:
        st.metric("📙 Actifs avec expiration", nb_active_exp)
    with col5:
        st.metric("📕 Brevets expirés", nb_expired)

# 🔄 **Suivi en temps réel**
st.subheader("⏳ Suivi en temps réel des traitements")
st.text("🔄 Tâche en cours d’exécution : Extraction et analyse des brevets...")

# 🔍 **Filtres latéraux**
st.sidebar.title("🎛️ Filtres")

# ✅ **Filtrer par date de publication**
if "Date de publication" in df.columns:
    df["Date de publication"] = pd.to_datetime(df["Date de publication"], errors='coerce')
    if not df["Date de publication"].isnull().all():
        min_date = df["Date de publication"].min().to_pydatetime()
        max_date = df["Date de publication"].max().to_pydatetime()
        date_range = st.sidebar.slider("📅 Filtrer par période", min_value=min_date, max_value=max_date, value=(min_date, max_date))
        df = df[(df["Date de publication"] >= date_range[0]) & (df["Date de publication"] <= date_range[1])]

# ✅ **Filtrer par titulaire du brevet**
if "Titulaire du brevet" in df.columns:
    assignees = st.sidebar.multiselect("🏢 Filtrer par organisation", df["Titulaire du brevet"].dropna().unique())
    if assignees:
        df = df[df["Titulaire du brevet"].isin(assignees)]

# ✅ **Filtrer par domaine technologique**
if "Domaine Technologique" in df.columns:
    domains = st.sidebar.multiselect("🧪 Filtrer par domaine technologique", df["Domaine Technologique"].dropna().unique())
    if domains:
        df = df[df["Domaine Technologique"].isin(domains)]

# 📈 **Graphique des brevets par année**
st.subheader("📈 Nombre de brevets par année")
if "Date de publication" in df.columns and not df["Date de publication"].isnull().all():
    brevet_par_annee = df.groupby(df["Date de publication"].dt.year).size().reset_index(name="Nombre de brevets")
    fig = px.line(brevet_par_annee, x="Date de publication", y="Nombre de brevets", title="📅 Évolution des brevets 6G par année")
    st.plotly_chart(fig, use_container_width=True)

# ☁ **Word Cloud des mots-clés**
st.subheader("☁ Mots-clés les plus populaires")
if "Mots-clés" in df.columns and not df["Mots-clés"].isnull().all():
    text = " ".join(df["Mots-clés"].dropna())
    wc = wordcloud.WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

# 🏆 **Organisation la plus active**
st.subheader("🏆 Organisation ayant déposé le plus de brevets")
if "Titulaire du brevet" in df.columns:
    top_assignee = df["Titulaire du brevet"].value_counts().idxmax()
    top_count = df["Titulaire du brevet"].value_counts().max()
    st.success(f"📌 **{top_assignee}** avec **{top_count} brevets** déposés !")

# 🥧 **Répartition des domaines technologiques**
st.subheader("📊 Répartition des brevets par domaine technologique")
if "Domaine Technologique" in df.columns:
    domain_counts = df["Domaine Technologique"].value_counts().reset_index()
    domain_counts.columns = ["Domaine Technologique", "Nombre de brevets"]
    fig = px.pie(domain_counts, names="Domaine Technologique", values="Nombre de brevets",
                 title="📡 Répartition des brevets par domaine technologique", hole=0.3)
    st.plotly_chart(fig, use_container_width=True)

# 📄 **Modifier et Télécharger le fichier**
st.subheader("📄 Modifier et Télécharger les données")
edit_df = st.data_editor(df)
st.download_button("📥 Télécharger les données modifiées", edit_df.to_csv(index=False), "brevets_6G_modifiés.csv", "text/csv")

# 🏁 Footer avec copyright
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("© 2025 - UTHAYAKUMAR Kelvin, DIARRASSOUBA Yann, FALL Habdallahi, DANTON Emmanuel, DA COSTA SA Edmilson - 🚀", unsafe_allow_html=True)
