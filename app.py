from http.server import BaseHTTPRequestHandler, HTTPServer
import requests


class Server(BaseHTTPRequestHandler):

    def do_GET(self):

        # Check URL
        username = self.path.strip("/")

        if not username:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Username is required")
            return

        # Call GitHub API
        url = f"https://api.github.com/users/{username}/gists"

        try:
            # Timeout prevents the application from waiting forever
            response = requests.get(url, timeout=10)

        except requests.RequestException:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(b"GitHub API unavailable")
            return

        # GitHub user not found
        if response.status_code == 404:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"User not found")
            return

        # Return other GitHub errors as they are
        if response.status_code != 200:
            self.send_response(response.status_code)
            self.end_headers()
            self.wfile.write(response.content)
            return

        # Success
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response.content)


if __name__ == "__main__":
    # Application runs on port 8080
    server = HTTPServer(("0.0.0.0", 8080), Server)

    print("Server running on port 8080")

    server.serve_forever()