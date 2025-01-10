# import json
# import bcrypt
# import psycopg2
# from psycopg2.extras import DictCursor

DB_CONFIG = {
    'dbname': 'notchpay',
    'user': 'germann',
    'password': '12345',
    'host': 'localhost',
    'port': '5432'
}

# def get_db_connection():
#     """Crée et retourne une connexion à la base de données"""
#     return psycopg2.connect(**DB_CONFIG)


# def init_db():
#     """Initialise la base de données avec la table users"""
#     conn = get_db_connection()
#     cur = conn.cursor()
    
#     # # Création de la table users si elle n'existe pas
#     # cur.execute('''
#     #     CREATE TABLE IF NOT EXISTS users (
#     #         id SERIAL PRIMARY KEY,
#     #         username VARCHAR(50) UNIQUE NOT NULL,
#     #         password VARCHAR(255) NOT NULL,
#     #         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     #     )
#     # ''')
    
#     conn.commit()
#     cur.close()
#     conn.close()



# db.py
import psycopg2
from psycopg2.extras import DictCursor
from contextlib import contextmanager

# # Configuration de la base de données
# DB_CONFIG = {
#     'dbname': 'your_database_name',
#     'user': 'your_username',
#     'password': 'your_password',
#     'host': 'localhost',
#     'port': '5432'
# }

def get_db_connection():
    """Crée une connexion à la base de données"""
    return psycopg2.connect(**DB_CONFIG)

@contextmanager
def get_db_cursor():
    """
    Context manager pour obtenir un curseur de base de données.
    Gère automatiquement la connexion, les commits et la fermeture.
    """
    conn = None
    try:
        conn = get_db_connection()
        # DictCursor permet d'accéder aux résultats comme un dictionnaire
        cur = conn.cursor(cursor_factory=DictCursor)
        yield cur
        conn.commit()
    except Exception:
        if conn:
            conn.rollback()
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()