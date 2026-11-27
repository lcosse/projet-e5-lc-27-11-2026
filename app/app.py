from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def accueil():
    return jsonify({
        "application": "E5 E-commerce",
        "auteur": "LC",
        "statut": "Application Flask opérationnelle"
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/products")
def products():
    return jsonify([
        {"id": 1, "nom": "Ordinateur", "prix": 899},
        {"id": 2, "nom": "Clavier", "prix": 79},
        {"id": 3, "nom": "Souris", "prix": 39}
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
