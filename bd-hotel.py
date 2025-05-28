import sqlite3

conn = sqlite3.connect('hotel.db')
cursor = conn.cursor()


cursor.executescript("""
DROP TABLE IF EXISTS Concerner;
DROP TABLE IF EXISTS Evaluation;
DROP TABLE IF EXISTS Reservation;
DROP TABLE IF EXISTS Offre;
DROP TABLE IF EXISTS Chambre;
DROP TABLE IF EXISTS Type_Chambre;
DROP TABLE IF EXISTS Prestation;
DROP TABLE IF EXISTS Client;
DROP TABLE IF EXISTS Hotel;
""")


cursor.executescript("""
CREATE TABLE Hotel (
    Id_Hotel INTEGER PRIMARY KEY,
    Ville TEXT,
    Pays TEXT,
    Code_Postal INTEGER
);

CREATE TABLE Type_Chambre (
    Id_Type INTEGER PRIMARY KEY,
    Type TEXT,
    Tarif REAL
);

CREATE TABLE Chambre (
    Id_Chambre INTEGER PRIMARY KEY,
    Numero INTEGER,
    Etage INTEGER,
    Fumeurs BOOLEAN,
    Id_Hotel INTEGER,
    Id_Type INTEGER,
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel),
    FOREIGN KEY (Id_Type) REFERENCES Type_Chambre(Id_Type)
);

CREATE TABLE Prestation (
    Id_Prestation INTEGER PRIMARY KEY,
    Prix INTEGER,
    Description TEXT
);

CREATE TABLE Offre (
    Id_Hotel INTEGER,
    Id_Prestation INTEGER,
    PRIMARY KEY (Id_Hotel, Id_Prestation),
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel),
    FOREIGN KEY (Id_Prestation) REFERENCES Prestation(Id_Prestation)
);

CREATE TABLE Client (
    Id_Client INTEGER PRIMARY KEY,  
    Adresse TEXT,
    Ville TEXT,
    Code_Postal TEXT,
    E_mail TEXT,
    Num_Tele TEXT,
    Nom_Complet TEXT
);

CREATE TABLE Evaluation (
    Id_Evaluation INTEGER PRIMARY KEY,
    Date_Arrivee DATE,
    Note INTEGER,
    Commentaire TEXT,
    Id_Hotel INTEGER,
    Id_Client INTEGER,
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel),
    FOREIGN KEY (Id_Client) REFERENCES Client(Id_Client)
);

CREATE TABLE Reservation (
    Id_Reservation INTEGER PRIMARY KEY,
    Date_Arrivee DATE,
    Date_Depart DATE,
    Id_Client INTEGER,
    Id_Chambre INTEGER,
    FOREIGN KEY (Id_Client) REFERENCES Client(Id_Client),
    FOREIGN KEY (Id_Chambre) REFERENCES Chambre(Id_Chambre)
);

CREATE TABLE Concerner (
    Id_Prestation INTEGER,
    Id_Reservation INTEGER,
    PRIMARY KEY (Id_Prestation, Id_Reservation),
    FOREIGN KEY (Id_Prestation) REFERENCES Prestation(Id_Prestation),
    FOREIGN KEY (Id_Reservation) REFERENCES Reservation(Id_Reservation)
);
""")

# Insertion des données
cursor.executescript("""
INSERT INTO Hotel VALUES
(1, 'Paris', 'France', 75001),
(2, 'Lyon', 'France', 69002);

INSERT INTO Client VALUES
(1, '12 Rue de Paris', 'Paris', '75001', 'jean.dupont@email.fr', '0612345678', 'Jean Dupont'),
(2, '5 Avenue Victor Hugo', 'Lyon', '69002', 'marie.leroy@email.fr', '0623456789', 'Marie Leroy'),
(3, '8 Boulevard Saint-Michel', 'Marseille', '13005', 'paul.moreau@email.fr', '0634567890', 'Paul Moreau'),
(4, '27 Rue Nationale', 'Lille', '59800', 'lucie.martin@email.fr', '0645678901', 'Lucie Martin'),
(5, '3 Rue des Fleurs', 'Nice', '06000', 'emma.giraud@email.fr', '0656789012', 'Emma Giraud');

INSERT INTO Prestation VALUES
(1, 15, 'Petit-déjeuner'),
(2, 30, 'Navette aéroport'),
(3, 0, 'Wi-Fi gratuit'),
(4, 50, 'Spa et bien-être'),
(5, 20, 'Parking sécurisé');

INSERT INTO Type_Chambre VALUES
(1, 'Simple', 80),
(2, 'Double', 120);

INSERT INTO Chambre VALUES
(1, 201, 2, 0, 1, 1),
(2, 502, 5, 1, 1, 2),
(3, 305, 3, 0, 2, 1),
(4, 410, 4, 0, 2, 2),
(5, 104, 1, 1, 2, 2),
(6, 202, 2, 0, 1, 1),
(7, 307, 3, 1, 1, 2),
(8, 101, 1, 0, 1, 1);

INSERT INTO Reservation VALUES
(1, '2025-06-15', '2025-06-18', 1, 1),
(2, '2025-07-01', '2025-07-05', 2, 2),
(3, '2025-08-10', '2025-08-14', 3, 3),
(4, '2025-09-05', '2025-09-07', 4, 4),
(5, '2025-09-20', '2025-09-25', 5, 5),
(7, '2025-11-12', '2025-11-14', 2, 7),
(9, '2026-01-15', '2026-01-18', 4, 8),
(10, '2026-02-01', '2026-02-05', 2, 6);

INSERT INTO Evaluation VALUES
(1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1, 1),
(2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 1, 2),
(3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 2, 3),
(4, '2025-09-05', 5, 'Service impeccable, je recommande.', 2, 4),
(5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 2, 5);

INSERT INTO Offre VALUES 
(1, 1), (1, 3), 
(2, 1), (2, 2), (2, 3), (2, 5);

INSERT INTO Concerner VALUES 
(1, 1), (3, 1),
(1, 2), (5, 2),
(3, 3),
(1, 4), (2, 4), (4, 4),
(1, 5);
""")

# Commit et fermeture
conn.commit()
conn.close()

print("Base de données SQLite 'hotel.db' créée avec succès.")
