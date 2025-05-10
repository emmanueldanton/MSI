# MSI
📌 Description

Cette application Streamlit permet d'explorer, d'analyser et de visualiser les données relatives aux brevets 6G à partir d'un fichier CSV. Elle propose plusieurs indicateurs clés, des graphiques interactifs et des options de filtrage pour faciliter l'analyse des tendances en matière de brevets.

🚀 Fonctionnalités

Affichage des indicateurs clés : Nombre total de brevets, brevets actifs, expirés, etc.

Filtrage interactif : Filtrage des brevets par date de publication, titulaire et domaine technologique.

Visualisations interactives : Graphiques de l'évolution des brevets par année, nuage de mots des mots-clés et répartition des domaines technologiques.

Analyse des organisations les plus actives : Identification de l'organisation ayant déposé le plus de brevets.

Modification et exportation des données : Édition du tableau de brevets et téléchargement des données modifiées.

📂 Installation

1️⃣ Prérequis

Assurez-vous d'avoir installé Python et les bibliothèques suivantes :

pip install streamlit pandas plotly wordcloud matplotlib

2️⃣ Exécution de l'application

Exécutez la commande suivante dans le terminal :

streamlit run app.py

📁 Structure du projet

📂 Projet_Brevets_6G
│── app.py  # Code principal de l'application Streamlit
│── brevets_6Gfinal2.csv  # Fichier CSV contenant les données des brevets
│── README.md  # Documentation du projet

📝 Utilisation

Lancez l'application : streamlit run app.py

Chargez le fichier CSV : L'application tentera d'ouvrir brevets_6G.csv

Explorez les données via les tableaux, filtres et visualisations interactives

Modifiez les données dans le tableau éditable

Téléchargez le fichier modifié pour l'enregistrer en local

⚠️ Problèmes possibles

Fichier CSV introuvable : Vérifiez que brevets_6G.csv est bien dans le même dossier que app.py.

Colonnes manquantes : Assurez-vous que votre fichier contient les colonnes attendues (Date de publication, Statut du brevet, etc.).

Données incorrectes : Les dates doivent être dans un format lisible (YYYY-MM-DD) pour être traitées correctement.

📌 Auteurs
DANTON Emmanuel

DA COSTA SA Edmilson

UTHAYAKUMAR Kelvin

DIARRASSOUBA Yann

FALL Habdallahi



© 2025 - Tous droits réservés 🚀

