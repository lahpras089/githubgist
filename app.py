from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json


class Server(BaseHTTPRequestHandler):

    def do_GET(self):

        username = self.path.strip("/")

        url = f"https://api.github.com/users/{username}/gists"

        response = requests.get(url, timeout=10)

        self.send_response(response.status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(response.content)


server = HTTPServer(("0.0.0.0", 8080), Server)

print("Server running on port 8080")

server.serve_forever()