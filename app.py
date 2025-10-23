from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

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
    app.run(debug=True, host="0.0.0.0", port=666)
