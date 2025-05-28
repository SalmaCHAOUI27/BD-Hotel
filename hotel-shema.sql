-- Création de la base de données
CREATE DATABASE IF NOT EXISTS hotel_management;
USE hotel_management;

-- Suppression des tables si elles existent (pour réinitialiser)
DROP TABLE IF EXISTS Evaluation;
DROP TABLE IF EXISTS Reservation_Prestation;
DROP TABLE IF EXISTS Reservation_Chambre;
DROP TABLE IF EXISTS Reservation;
DROP TABLE IF EXISTS Chambre;
DROP TABLE IF EXISTS Type_Chambre;
DROP TABLE IF EXISTS Prestation;
DROP TABLE IF EXISTS Client;
DROP TABLE IF EXISTS Hotel;

-- Création des tables

-- Table Hotel

CREATE TABLE Hotel (
    id_hotel INT PRIMARY KEY AUTO_INCREMENT,
    ville VARCHAR(100) NOT NULL,
    pays VARCHAR(100) NOT NULL,
    code_postal VARCHAR(10)
);

-- Table Client
CREATE TABLE Client (
    id_client INT PRIMARY KEY AUTO_INCREMENT,

    adresse VARCHAR(255),
    ville VARCHAR(100),
    code_postal VARCHAR(10),
    email VARCHAR(150) UNIQUE,
    telephone VARCHAR(20),
    nom VARCHAR(100) NOT NULL
);

-- Table Prestation
CREATE TABLE Prestation (
    id_prestation INT PRIMARY KEY AUTO_INCREMENT,
    prix DECIMAL(10,2) NOT NULL,
    nom VARCHAR(100) NOT NULL
);

-- Table Type_Chambre
CREATE TABLE Type_Chambre (
    id_type INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(50) NOT NULL,
    prix_nuit DECIMAL(10,2) NOT NULL
);

-- Table Chambre
CREATE TABLE Chambre (
    id_chambre INT PRIMARY KEY AUTO_INCREMENT,
    numero INT NOT NULL,
    etage INT,
    vue_mer BOOLEAN DEFAULT FALSE,
    id_hotel INT,
    id_type INT,
    FOREIGN KEY (id_hotel) REFERENCES Hotel(id_hotel),
    FOREIGN KEY (id_type) REFERENCES Type_Chambre(id_type)
);

-- Table Reservation

CREATE TABLE Reservation (
    id_reservation INT PRIMARY KEY AUTO_INCREMENT,
    date_debut DATE NOT NULL,
    date_fin DATE NOT NULL,
    id_client INT,
    FOREIGN KEY (id_client) REFERENCES Client(id_client)
);

-- Table de liaison Reservation_Chambre (relation N:M)
CREATE TABLE Reservation_Chambre (
    id_reservation INT,
    id_chambre INT,
    PRIMARY KEY (id_reservation, id_chambre),
    FOREIGN KEY (id_reservation) REFERENCES Reservation(id_reservation),
    FOREIGN KEY (id_chambre) REFERENCES Chambre(id_chambre)
);

-- Table de liaison Reservation_Prestation (relation N:M)
CREATE TABLE Reservation_Prestation (
    id_reservation INT,
    id_prestation INT,
    quantite INT DEFAULT 1,
    PRIMARY KEY (id_reservation, id_prestation),
    FOREIGN KEY (id_reservation) REFERENCES Reservation(id_reservation),
    FOREIGN KEY (id_prestation) REFERENCES Prestation(id_prestation)
);

-- Table Evaluation
CREATE TABLE Evaluation (
    id_evaluation INT PRIMARY KEY AUTO_INCREMENT,
    date_evaluation DATE NOT NULL,
    note INT CHECK (note >= 1 AND note <= 5),
    commentaire TEXT,
    id_client INT,
    FOREIGN KEY (id_client) REFERENCES Client(id_client)
);

-- Insertion des données

-- Données Hotel
INSERT INTO Hotel (id_hotel, ville, pays, code_postal) VALUES
(1, 'Paris', 'France', '75001'),
(2, 'Lyon', 'France', '69002');

-- Données Client

INSERT INTO Client (id_client, adresse, ville, code_postal, email, telephone, nom) VALUES
(1, '12 Rue de Paris', 'Paris', '75001', 'jean.dupont@email.fr', '0612345678', 'Jean Dupont'),
(2, '5 Avenue Victor Hugo', 'Lyon', '69002', 'marie.leroy@email.fr', '0623456789', 'Marie Leroy'),
(3, '8 Boulevard Saint-Michel', 'Marseille', '13005', 'paul.moreau@email.fr', '0634567890', 'Paul Moreau'),
(4, '27 Rue Nationale', 'Lille', '59800', 'lucie.martin@email.fr', '0645678901', 'Lucie Martin'),
(5, '3 Rue des Fleurs', 'Nice', '06000', 'emma.giraud@email.fr', '0656789012', 'Emma Giraud');

-- Données Prestation

INSERT INTO Prestation (id_prestation, prix, nom) VALUES
(1, 15.00, 'Petit-déjeuner'),
(2, 30.00, 'Navette aéroport'),
(3, 0.00, 'Wi-Fi gratuit'),
(4, 50.00, 'Spa et bien-être'),
(5, 20.00, 'Parking sécurisé');

-- Données Type_Chambre
INSERT INTO Type_Chambre (id_type, nom, prix_nuit) VALUES
(1, 'Simple', 80.00),
(2, 'Double', 120.00);

-- Données Chambre
INSERT INTO Chambre (id_chambre, numero, etage, vue_mer, id_hotel, id_type) VALUES
(1, 201, 2, FALSE, 1, 1),
(2, 502, 5, TRUE, 1, 2),
(3, 305, 3, FALSE, 2, 1),
(4, 410, 4, FALSE, 2, 2),
(5, 104, 1, TRUE, 2, 2),
(6, 202, 2, FALSE, 1, 1),
(7, 307, 3, TRUE, 1, 2),
(8, 101, 1, FALSE, 1, 1);

-- Données Reservation


INSERT INTO Reservation (id_reservation, date_debut, date_fin, id_client) VALUES
(1, '2025-06-15', '2025-06-18', 1),
(2, '2025-07-01', '2025-07-05', 2),
(3, '2025-08-10', '2025-08-14', 3),
(4, '2025-09-05', '2025-09-07', 4),
(5, '2025-09-20', '2025-09-25', 5),
(7, '2025-11-12', '2025-11-14', 2),
(9, '2026-01-15', '2026-01-18', 4),
(10, '2026-02-01', '2026-02-05', 2);

-- Liaison Reservation_Chambre (exemple - à adapter selon vos besoins)
INSERT INTO Reservation_Chambre (id_reservation, id_chambre) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (7, 7), (9, 4), (10, 2);

-- Données Evaluation
INSERT INTO Evaluation (id_evaluation, date_evaluation, note, commentaire, id_client) VALUES
(1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1),
(2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),
(3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),
(4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4),
(5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5);

-- REQUÊTES SQL DEMANDÉES


-- |. Afficher la liste des réservations avec le nom du client et la ville de l'hôtel réservé
SELECT 
    r.id_reservation,
    c.nom AS nom_client,
    r.date_debut,
    r.date_fin,
    h.ville AS ville_hotel
FROM Reservation r
JOIN Client c ON r.id_client = c.id_client
JOIN Reservation_Chambre rc ON r.id_reservation = rc.id_reservation
JOIN Chambre ch ON rc.id_chambre = ch.id_chambre
JOIN Hotel h ON ch.id_hotel = h.id_hotel;

-- ||. Afficher les clients qui habitent à Paris
SELECT *
FROM Client
WHERE ville = 'Paris';

-- |||. Calculer le nombre de réservations faites par chaque client
SELECT 
    c.nom,
    COUNT(r.id_reservation) AS nombre_reservations
FROM Client c
LEFT JOIN Reservation r ON c.id_client = r.id_client
GROUP BY c.id_client, c.nom
ORDER BY nombre_reservations DESC;

-- |||. Donner le nombre de chambres pour chaque type de chambre
SELECT 
    tc.nom AS type_chambre,
    COUNT(ch.id_chambre) AS nombre_chambres
FROM Type_Chambre tc
LEFT JOIN Chambre ch ON tc.id_type = ch.id_type
GROUP BY tc.id_type, tc.nom;

-- ||||. Afficher la liste des chambres qui ne sont pas réservées pour une période donnée

-- la période du 2025-07-01 au 2025-07-31
SELECT DISTINCT
    ch.id_chambre,
    ch.numero,
    h.ville AS hotel_ville,
    tc.nom AS type_chambre
FROM Chambre ch
JOIN Hotel h ON ch.id_hotel = h.id_hotel
JOIN Type_Chambre tc ON ch.id_type = tc.id_type
WHERE ch.id_chambre NOT IN (
    SELECT DISTINCT rc.id_chambre
    FROM Reservation_Chambre rc
    JOIN Reservation r ON rc.id_reservation = r.id_reservation
    WHERE (r.date_debut <= '2025-07-31' AND r.date_fin >= '2025-07-01')
);
