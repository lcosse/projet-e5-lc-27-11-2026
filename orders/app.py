from flask import Flask, jsonify

app = Flask(__name__)

commandes = [
    {"id": 1, "client": "Client 1", "produit": "Ordinateur", "statut": "Expédiée"},
    {"id": 2, "client": "Client 2", "produit": "Clavier", "statut": "En préparation"},
    {"id": 3, "client": "Client 3", "produit": "Souris", "statut": "Livrée"}
]

@app.route("/")
def accueil():
    return jsonify({
        "application": "E5 Suivi des commandes",
        "auteur": "LC",
        "status": "Application opérationnelle"
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/orders")
def afficher_commandes():
    return jsonify(commandes)

@app.route("/orders/<int:commande_id>")
def detail_commande(commande_id):
    for commande in commandes:
        if commande["id"] == commande_id:
            return jsonify(commande)

    return jsonify({"erreur": "Commande introuvable"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5007)
