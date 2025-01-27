# api/handlers.py
from http.server import BaseHTTPRequestHandler
import json
from .handler_auth import handle_register, handle_login

class SimpleAPIHandler(BaseHTTPRequestHandler):
    def _send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

     # Gestion des requêtes POST
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())

        if self.path == '/api/register':
            handle_register(self,data)
        elif self.path == '/api/login':
            handle_login(self,data)
        else:
            self._send_json_response(404, {"error": "Endpoint not found"})
    #     handle_login(data)

    
    def do_GET(self):
        if self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Exemple de données à retourner
            data = {
                "message": "Ceci est une réponse GETO",
                "status": "success"
            }
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_error(404, "Endpoint not found")

