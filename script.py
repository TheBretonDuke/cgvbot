import mysql.connector
from mysql.connector import Error

def main():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3307,
            user="root",
            password="example"
        )
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS fly_buzz;")
        cursor.execute("USE fly_buzz;")

        # Création des tables modifiées
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aeroports (
                id_aeroport INT AUTO_INCREMENT PRIMARY KEY,
                nom_aeroport VARCHAR(100) NOT NULL,
                id_ville VARCHAR(100) NOT NULL,
                nom_ville VARCHAR(100) NOT NULL,
                id_pays INT
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pilotes (
                id_pilote INT AUTO_INCREMENT PRIMARY KEY,
                nom_pilote VARCHAR(100) NOT NULL,
                prenom_pilote VARCHAR(100) NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS avions (
                id_avion INT AUTO_INCREMENT PRIMARY KEY,
                numero_appareil VARCHAR(100) NOT NULL,
                modele VARCHAR(100) DEFAULT NULL,
                date_entree DATE DEFAULT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vols (
                id_vol INT AUTO_INCREMENT PRIMARY KEY,
                numero_vol VARCHAR(100) NOT NULL,
                depart INT,
                date_heure_depart DATETIME NOT NULL,
                arrivee INT,
                date_heure_arrivee DATETIME NOT NULL,
                FOREIGN KEY (depart) REFERENCES aeroports(id_aeroport),
                FOREIGN KEY (arrivee) REFERENCES aeroports(id_aeroport)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assigne (
                id_pilote INT,
                id_vol INT,
                PRIMARY KEY (id_pilote, id_vol),
                FOREIGN KEY (id_pilote) REFERENCES pilotes(id_pilote),
                FOREIGN KEY (id_vol) REFERENCES vols(id_vol)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS piloter (
                id_pilote INT,
                id_avion INT,
                PRIMARY KEY (id_pilote, id_avion),
                FOREIGN KEY (id_pilote) REFERENCES pilotes(id_pilote),
                FOREIGN KEY (id_avion) REFERENCES avions(id_avion)
            );
        """)

        # Insertion des aéroports
        aeroports = [
            ('Aéroport Charles de Gaulle', 'Paris', 'Paris', None),
            ('Aéroport de Rio de Janeiro', 'Rio de Janeiro', 'Rio de Janeiro', None),
            ('Aéroport de Sydney', 'Sydney', 'Sydney', None),
            ('Aéroport de Los Angeles', 'Los Angeles', 'Los Angeles', None),
            ('Aéroport de Kangerlussuaq', 'Kangerlussuaq', 'Kangerlussuaq', None),
        ]
        cursor.executemany(
            "INSERT INTO aeroports (nom_aeroport, id_ville, nom_ville, id_pays) VALUES (%s, %s, %s, %s)",
            aeroports
        )

        # Récupérer les IDs des aéroports (pour référence)
        cursor.execute("SELECT id_aeroport, nom_ville FROM aeroports;")
        aeroport_dict = {ville: id_aeroport for (id_aeroport, ville) in cursor.fetchall()}

        # Insertion des pilotes
        pilotes = [
            ('Striker', 'Ted'),
            ('Kramer', 'Rex'),
            ('Oveur', 'Clarence')
        ]
        cursor.executemany(
            "INSERT INTO pilotes (nom_pilote, prenom_pilote) VALUES (%s, %s)",
            pilotes
        )
        cursor.execute("SELECT id_pilote, nom_pilote FROM pilotes;")
        pilote_dict = {nom: id_pilote for (id_pilote, nom) in cursor.fetchall()}

        # Insertion des avions
        avions = [
            ('XW-01', None, None),
            ('XW-02', None, None),
            ('FS-07', None, None),
        ]
        cursor.executemany(
            "INSERT INTO avions (numero_appareil, modele, date_entree) VALUES (%s, %s, %s)",
            avions
        )
        cursor.execute("SELECT id_avion, numero_appareil FROM avions;")
        avion_dict = {num: id_avion for (id_avion, num) in cursor.fetchall()}

        # Insertion des vols
        vols = [
            ('MS291', aeroport_dict['Paris'], '2019-06-15 11:00:00', aeroport_dict['Rio de Janeiro'], '2019-06-15 22:40:00'),
            ('MS292', aeroport_dict['Sydney'], '2019-06-23 06:50:00', aeroport_dict['Los Angeles'], '2019-06-23 19:36:00'),
            ('MS293', aeroport_dict['Paris'], '2019-06-28 16:40:00', aeroport_dict['Kangerlussuaq'], '2019-06-29 09:05:00'),
        ]
        cursor.executemany(
            "INSERT INTO vols (numero_vol, depart, date_heure_depart, arrivee, date_heure_arrivee) VALUES (%s, %s, %s, %s, %s)",
            vols
        )

        # Récupérer IDs des vols pour les associer aux pilotes et avions
        cursor.execute("SELECT id_vol, numero_vol FROM vols;")
        vol_dict = {num: id_vol for (id_vol, num) in cursor.fetchall()}

        # Assigner les pilotes aux vols
        assigne = [
            (pilote_dict['Striker'], vol_dict['MS291']),
            (pilote_dict['Kramer'], vol_dict['MS291']),
            (pilote_dict['Kramer'], vol_dict['MS292']),
            (pilote_dict['Oveur'], vol_dict['MS292']),
            (pilote_dict['Kramer'], vol_dict['MS293']),
            (pilote_dict['Oveur'], vol_dict['MS293']),
        ]
        cursor.executemany(
            "INSERT INTO assigne (id_pilote, id_vol) VALUES (%s, %s)",
            assigne
        )

        # Assigner les pilotes aux avions
        piloter = [
            (pilote_dict['Striker'], avion_dict['XW-01']),
            (pilote_dict['Kramer'], avion_dict['XW-02']),
            (pilote_dict['Oveur'], avion_dict['FS-07']),
        ]
        cursor.executemany(
            "INSERT INTO piloter (id_pilote, id_avion) VALUES (%s, %s)",
            piloter
        )

        conn.commit()
        print("Données vols, pilotes, avions, aéroports insérées avec succès.")

    except Error as e:
        print(f"Erreur : {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Connexion MySQL fermée.")

if __name__ == "__main__":
    main()
