from flask import Flask, jsonify
import requests

app = Flask(__name__)


@app.route("/<username>")
def get_gists(username):

    url = f"https://api.github.com/users/{username}/gists"

    response = requests.get(url)

    if response.status_code == 404:
        return jsonify({"error": "User not found"}), 404

    gists = response.json()

    return jsonify(gists)


app.run(host="0.0.0.0", port=8080)