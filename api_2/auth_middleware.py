# auth_middleware.py
import jwt
from datetime import datetime, timedelta
from functools import wraps

JWT_SECRET = "votre_secret_key"
JWT_ALGORITHM = "HS256"

def require_auth(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        auth_header = self.headers.get('Authorization')
        
        if not auth_header:
            self._send_json_response(401, {"error": "Authentication required"})
            return

        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            self.user = payload
            return func(self, *args, **kwargs)
        except Exception as e:
            self._send_json_response(401, {"error": str(e)})
            return
    return wrapper