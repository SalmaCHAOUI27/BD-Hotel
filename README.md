# 🏨 Projet de Gestion Hôtelière

Ce projet est une **application web de gestion hôtelière** développée avec [Streamlit](https://streamlit.io) et utilisant une base de données **SQLite**.

---

## 🔧 Fonctionnalités

L’application permet de :

- 📋 Afficher la **liste des clients**
- 📅 Afficher les **réservations existantes**
- 🛏️ Voir les **chambres disponibles** pour une période donnée
- ➕ **Ajouter de nouveaux clients**
- 🛎️ **Créer de nouvelles réservations**

---

## 📁 Structure du projet

```
Projet-BasesDonnees/
│
├── app.py                  # Interface Streamlit principale
├── bd-hotel.py             # Script alternatif de génération SQLite
├── hotel-shema.sql         # Script SQL de création des tables + données
├── hotel_management.db     # Base de données utilisée par l'application
├── hotel.db                # Ancienne base (peut être ignorée)
├── insertion.sqlite        # Fichier de données (optionnel)
└── README.md               # Fichier d'explication du projet
```

---

## 🚀 Lancer l'application

1. Assurez-vous que Python est installé (version 3.8 ou plus recommandée)
2. Installez **Streamlit** si nécessaire :
   ```bash
   pip install streamlit
   ```

3. Lancez l'application :
   ```bash
   streamlit run app.py
   ```

4. Une page s'ouvrira dans le navigateur à l'adresse :
   ```
   http://localhost:8501
   ```

---

## 🧠 Données initiales

Les données sont insérées automatiquement lors du **premier lancement** à partir du fichier `hotel-shema.sql`, y compris :

- Des hôtels (Paris, Lyon…)
- Des clients avec leurs adresses
- Des chambres par type
- Des prestations
- Des réservations déjà existantes

---

## ✨ Interface Utilisateur

L'application propose une navigation via un menu latéral :

- **Accueil 🏠** : Présentation de l'application
- **Clients 👥** : Liste des clients enregistrés
- **Réservations 📅** : Affichage des réservations
- **Chambres disponibles 🛏️** : Recherche des chambres libres entre deux dates
- **Ajouter Client ➕** : Formulaire pour ajouter un nouveau client
- **Ajouter une réservation 🛎️** : Sélection d'un client et d'une chambre pour réserver

---

## 👩‍💻 Réalisé par

> ✨ *Salma CHAOUI*  
> Étudiante en FSSM
