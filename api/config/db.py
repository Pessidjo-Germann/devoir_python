import json
import bcrypt
import psycopg2
from psycopg2.extras import DictCursor

DB_CONFIG = {
    'dbname': 'notchpay',
    'user': 'germann',
    'password': '12345',
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    """Crée et retourne une connexion à la base de données"""
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    """Initialise la base de données avec la table users"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # # Création de la table users si elle n'existe pas
    # cur.execute('''
    #     CREATE TABLE IF NOT EXISTS users (
    #         id SERIAL PRIMARY KEY,
    #         username VARCHAR(50) UNIQUE NOT NULL,
    #         password VARCHAR(255) NOT NULL,
    #         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #     )
    # ''')
    
    conn.commit()
    cur.close()
    conn.close()