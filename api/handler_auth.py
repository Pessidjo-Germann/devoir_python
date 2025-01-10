import json
from api.config.db import get_db_connection
import bcrypt
import psycopg2

# Exemple de base de données en mémoire (pour la démo)
users_db = []

def handle_register(self, data):
    """
    Gère la création de compte (register).
    """
    username = data.get('username')
    password = data.get('password')
    
    try:
        conn=get_db_connection()
        cur=conn.cursor()

         # Vérifier si l'utilisateur existe déjà
        cur.execute("SELECT username FROM usero WHERE username = %s", (username,))
        if cur.fetchone():
            self._send_json_response(400, {"error": "Username already exists"})
            return

        # Hacher le mot de passe avant de le stocker
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        
        # Insérer le nouvel utilisateur
        cur.execute(
            "INSERT INTO usero (username, password) VALUES (%s, %s)",
            (username, hashed_password.decode())
        )
        
        conn.commit()
        self._send_json_response(201, {"message": "User registered successfully"})

    except psycopg2.Error as e:
        conn.rollback()
        self._send_json_response(500, {"error": f"Database error: {str(e)}"})
    finally:
        pass
        #cur.close()
        #conn.close()

def handle_login(self, data):
    """
    Gère la connexion (login).
    """
    card_number = data.get('card_number')
    pin = data.get('pin')

    if not card_number or not pin:
        self._send_json_response(400, {"error": "Veuillez entrer vos iinformations pour vous connecter!"})
        return

    try:
        #init db
        conn=get_db_connection()
        cur=conn.cursor()

        cur.execute("select * from card where card_number =%s,"(card_number,))
        if cur.rowcount==0:
            self._send_json_response(401,{"error":"Desole aucun compte n'existe avec ce numerp de card"})
            return
        
        card=cur.fetchone()
        store_pin=card['cvv']

        # Vérifier le mot de passe
        if bcrypt.checkpw(pin.encode(), store_pin.encode()):
            # Créer une réponse avec plus d'informations (optionnel)
            response_data = {
                "message": "Connexion reussie",
                "user": {
                    "id": card['card_number'],
                    "username": card['cvv']
                }
                # Vous pouvez ajouter d'autres champs ici si nécessaire
            }
            
            self._send_json_response(200, response_data)
        else:
            self._send_json_response(401, {"error": "Invalid card number"})

    except psycopg2.Error as e:
        self._send_json_response(405, {"error": "Erreur lors du log"})
    finally:
        pass
    # Trouver l'utilisateur dans la base de données

