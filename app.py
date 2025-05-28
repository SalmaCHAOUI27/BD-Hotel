import streamlit as st
import sqlite3
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Hôtel App", page_icon="🏨", layout="wide")

DB_NAME = 'hotel_management.db'

def init_db():
    if os.path.exists(DB_NAME):
        return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.executescript(open("hotel-shema.sql", encoding="utf-8").read())
    conn.commit()
    conn.close()

def connect():
    return sqlite3.connect(DB_NAME)

def get_clients():
    return pd.read_sql_query("SELECT * FROM Client", connect())

def get_reservations():
    return pd.read_sql_query('''
        SELECT r.id_reservation, c.nom, r.date_debut, r.date_fin, h.ville
        FROM Reservation r
        JOIN Client c ON r.id_client = c.id_client
        JOIN Reservation_Chambre rc ON rc.id_reservation = r.id_reservation
        JOIN Chambre ch ON ch.id_chambre = rc.id_chambre
        JOIN Hotel h ON ch.id_hotel = h.id_hotel
    ''', connect())

def get_available_rooms(start, end):
    return pd.read_sql_query('''
        SELECT ch.id_chambre, ch.numero, h.ville
        FROM Chambre ch
        JOIN Hotel h ON h.id_hotel = ch.id_hotel
        WHERE ch.id_chambre NOT IN (
            SELECT rc.id_chambre
            FROM Reservation r
            JOIN Reservation_Chambre rc ON r.id_reservation = rc.id_reservation
            WHERE r.date_debut <= ? AND r.date_fin >= ?
        )
    ''', connect(), params=[end, start])

def add_client(nom, adresse, ville, code_postal, email, telephone):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Client (nom, adresse, ville, code_postal, email, telephone) VALUES (?, ?, ?, ?, ?, ?)",
                   (nom, adresse, ville, code_postal, email, telephone))
    conn.commit()
    conn.close()

def main():
    st.title("🏨 Application Hôtelière - Bienvenue ! 🌟")
    init_db()

    menu = st.sidebar.selectbox("🧭 Navigation", [
        "Accueil 🏠", 
        "Clients 👥", 
        "Réservations 📅", 
        "Chambres disponibles 🛏️", 
        "Ajouter Client ➕", 
        "Ajouter une réservation 🛎️"
    ])

    if menu == "Accueil 🏠":
        st.title("🏨 Système de Gestion Hôtelière")
        st.write("Bienvenue dans le système de gestion hôtelière")
        st.write("Cette application vous permet de :")
        st.write("- Consulter les réservations existantes")
        st.write("- Voir la liste des clients")
        st.write("- Vérifier la disponibilité des chambres")
        st.write("- Ajouter de nouveaux clients")
        st.write("- Créer de nouvelles réservations")
        st.write("Utilisez le menu à gauche pour naviguer entre les différentes fonctionnalités.")

      

    elif menu == "Clients 👥":
        st.subheader("📋 Liste des clients")
        st.dataframe(get_clients())

    elif menu == "Réservations 📅":
        st.subheader("📋 Liste des réservations")
        st.dataframe(get_reservations())

    elif menu == "Chambres disponibles 🛏️":
        col1, col2 = st.columns(2)
        with col1:
            d1 = st.date_input("📅 Date de début", value=date.today())
        with col2:
            d2 = st.date_input("📅 Date de fin", value=date.today())
        if d1 < d2:
            st.dataframe(get_available_rooms(d1, d2))
        else:
            st.error("⚠️ La date de début doit être avant la date de fin")

    elif menu == "Ajouter Client ➕":
        st.subheader("➕ Ajouter un client")
        with st.form("form_client"):
            nom = st.text_input("👤 Nom complet *", placeholder="Ex: Jean Dupont")
            adresse = st.text_input("🏠 Adresse", placeholder="Ex: 12 Rue de la Paix")
            ville = st.text_input("🏙️ Ville", placeholder="Ex: Paris")
            code_postal = st.text_input("📮 Code postal", placeholder="Ex: 75001")
            email = st.text_input("📧 Email *", placeholder="Ex: jean.dupont@email.com")
            telephone = st.text_input("📞 Téléphone", placeholder="Ex: 0123456789")
            submit_client = st.form_submit_button("Ajouter")

            if submit_client:
                if nom and email:
                    add_client(nom, adresse, ville, code_postal, email, telephone)
                    st.success("✅ Client ajouté avec succès !")
                else:
                    st.error("⚠️ Le nom et l'email sont obligatoires")

    elif menu == "Ajouter une réservation 🛎️":
        st.subheader("➕ Ajouter une Réservation 🛎️")
        clients = get_clients()
        if clients.empty:
            st.warning("⚠️ Pas de clients disponibles, veuillez ajouter un client d'abord.")
        else:
            with st.form("form_reservation"):
                client_options = clients['nom'].tolist()
                client_selected = st.selectbox("👤 Sélectionnez un client", client_options)

                date_debut = st.date_input("📅 Date de début", value=date.today())
                date_fin = st.date_input("📅 Date de fin", value=date.today())

                if date_debut >= date_fin:
                    st.error("⚠️ La date de début doit être avant la date de fin")
                    chambre_selected = None
                else:
                    chambres_dispo = get_available_rooms(date_debut, date_fin)
                    if chambres_dispo.empty:
                        st.warning("❌ Aucune chambre disponible pour ces dates.")
                        chambre_selected = None
                    else:
                        chambre_options = chambres_dispo.apply(
                            lambda row: f"Chambre {row['numero']} - {row['ville']}", axis=1).tolist()
                        chambre_selected = st.selectbox("🏨 Sélectionnez une chambre disponible", chambre_options)

                submit_reservation = st.form_submit_button("📩 Ajouter la réservation")

            if submit_reservation:
                if chambre_selected and date_debut < date_fin:
                    id_client = clients[clients['nom'] == client_selected]['id_client'].values[0]
                    chambre_numero = int(chambre_selected.split()[1])
                    id_chambre = chambres_dispo[chambres_dispo['numero'] == chambre_numero]['id_chambre'].values[0]

                    conn = connect()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO Reservation (id_client, date_debut, date_fin) VALUES (?, ?, ?)",
                                   (id_client, date_debut, date_fin))
                    id_reservation = cursor.lastrowid
                    cursor.execute("INSERT INTO Reservation_Chambre (id_reservation, id_chambre) VALUES (?, ?)",
                                   (id_reservation, id_chambre))
                    conn.commit()
                    conn.close()
                    st.success("✅ Réservation ajoutée avec succès !")
                else:
                    st.error("⚠️ Veuillez corriger les erreurs avant de soumettre.")

if __name__ == "__main__":
    main()
