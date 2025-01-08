import json
import bcrypt

# Exemple de base de données en mémoire (pour la démo)
users_db = []

def handle_register(self, data):
    """
    Gère la création de compte (register).
    """
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        self._send_json_response(400, {"error": "Username and password are required"})
        return

    # Vérifier si l'utilisateur existe déjà
    if any(user['username'] == username for user in users_db):
        self._send_json_response(400, {"error": "Username already exists"})
        return

    # Hacher le mot de passe avant de le stocker
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users_db.append({"username": username, "password": hashed_password.decode()})
    self._send_json_response(201, {"message": "User registered successfully"})

def handle_login(self, data):
    """
    Gère la connexion (login).
    """
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        self._send_json_response(400, {"error": "Username and password are required"})
        return

    # Trouver l'utilisateur dans la base de données
    user = next((user for user in users_db if user['username'] == username), None)
    if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
        self._send_json_response(200, {"message": "Login successful"})
    else:
        self._send_json_response(401, {"error": "Invalid username or password"})
