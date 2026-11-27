import os
import stripe

from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "E5 E-commerce")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")

PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{{ app_name }}</title>
    <style>
        body {
            font-family: Arial;
            background: #f2f4f8;
            text-align: center;
            padding: 60px;
        }
        .card {
            background: white;
            max-width: 450px;
            margin: auto;
            padding: 35px;
            border-radius: 12px;
        }
        button {
            background: #635bff;
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 17px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>{{ app_name }}</h1>
        <h2>Pack découverte</h2>
        <h2>19,99 €</h2>
        <p>Paiement sécurisé avec Stripe</p>
        <form action="/create-checkout-session" method="POST">
            <button type="submit">Payer avec Stripe</button>
        </form>
    </div>
</body>
</html>
"""

@app.route("/")
def accueil():
    return render_template_string(PAGE, app_name=APP_NAME)

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

@app.route("/products")
def products():
    return [
        {"id": 1, "nom": "Pack découverte", "prix": 19.99}
    ]

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():

    if not STRIPE_SECRET_KEY.startswith("sk_test_"):
        return "Clé Stripe de test absente ou incorrecte", 503

    try:
        stripe.api_key = STRIPE_SECRET_KEY

        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": "Pack découverte E5"
                    },
                    "unit_amount": 1999
                },
                "quantity": 1
            }],
            success_url=request.host_url.rstrip("/")
                + "/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.host_url.rstrip("/") + "/cancel"
        )

        return redirect(session.url, code=303)

    except stripe.StripeError:
        app.logger.exception("Erreur Stripe")
        return "Impossible de créer la session de paiement", 502

@app.route("/success")
def success():
    return """
    <h1>Paiement réussi !</h1>
    <p>Merci pour votre commande.</p>
    <a href="/">Retour à la boutique</a>
    """

@app.route("/cancel")
def cancel():
    return """
    <h1>Paiement annulé</h1>
    <p>Votre paiement n'a pas été effectué.</p>
    <a href="/">Retour à la boutique</a>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
