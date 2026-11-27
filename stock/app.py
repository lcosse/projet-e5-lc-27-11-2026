from flask import Flask, jsonify, request

app = Flask(__name__)

# Stockage des produits en mémoire
stocks = [
    {"id": 1, "nom": "Ordinateur", "quantite": 15},
    {"id": 2, "nom": "Clavier", "quantite": 30},
    {"id": 3, "nom": "Souris", "quantite": 25}
]

@app.route("/")
def accueil():
    return jsonify({
        "application": "E5 Gestion des stocks",
        "auteur": "LC",
        "status": "Application opérationnelle"
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/stock")
def afficher_stock():
    return jsonify(stocks)

@app.route("/stock/<int:produit_id>")
def produit(produit_id):
    for item in stocks:
        if item["id"] == produit_id:
            return jsonify(item)
    return jsonify({"erreur": "Produit introuvable"}), 404

@app.route("/stock/<int:produit_id>", methods=["PUT"])
def modifier_stock(produit_id):
    donnees = request.get_json(silent=True) or {}

    for item in stocks:
        if item["id"] == produit_id:
            quantite = donnees.get("quantite")

            if not isinstance(quantite, int) or isinstance(quantite, bool) or quantite < 0:
                return jsonify({"erreur": "Quantite invalide"}), 400

            item["quantite"] = quantite
            return jsonify(item)

    return jsonify({"erreur": "Produit introuvable"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)
