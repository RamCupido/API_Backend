from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from db import get_connection

app = Flask(__name__)
CORS(app)

#Endpoint para el login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            return jsonify({"status": "success", "message": "Login correcto"})
        else:
            return jsonify({"status": "error", "message": "Credenciales inválidas"}), 401

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint para buscar personajes de Rick and Morty
@app.route("/rickmorty/search/<name>")
def rickandmortyAPI(name):
    url = f"https://rickandmortyapi.com/api/character/?name={name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "results" in data:
            # Devuelve el primer resultado
            return jsonify(data["results"][0])
        else:
            return jsonify({'error': f"No se encontró un personaje con el nombre '{name}'"})
    else:
        return jsonify({'error': 'Error al consumir la API externa'}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
