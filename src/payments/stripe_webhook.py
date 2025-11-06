import os, json, stripe
from pathlib import Path
from flask import Blueprint, request, jsonify
from src.metrics import db as metrics

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
ENDPOINT_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

bp = Blueprint("stripe_webhook", __name__)
DB_PATH = Path("data/users.json")

def _load_db():
    if not DB_PATH.exists():
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        DB_PATH.write_text(json.dumps({
            "premium_users": [],
            "free_users": [],
            "modes": {},
            "voice": {},
            "tiers": {},
            "xp": {},
            "bond": {}
        }, indent=2))
    data = json.loads(DB_PATH.read_text())
    # Ensure all keys exist for backward compatibility
    if "modes" not in data:
        data["modes"] = {}
    if "voice" not in data:
        data["voice"] = {}
    if "tiers" not in data:
        data["tiers"] = {}
    if "xp" not in data:
        data["xp"] = {}
    if "bond" not in data:
        data["bond"] = {}
    return data

def _save_db(data):
    DB_PATH.write_text(json.dumps(data, indent=2))

@bp.route("/stripe/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get("Stripe-Signature", "")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, ENDPOINT_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        telegram_id = str(session.get("metadata", {}).get("telegram_user_id", "")).strip()
        tier = session.get("metadata", {}).get("tier", "")  # BRONZE, SILVER, GOLD

        if telegram_id:
            db = _load_db()
            if telegram_id not in db["premium_users"]:
                db["premium_users"].append(telegram_id)
                if telegram_id in db.get("free_users", []):
                    db["free_users"].remove(telegram_id)
                # Preserve existing mode or default to SAFE
                if telegram_id not in db["modes"]:
                    db["modes"][telegram_id] = db["modes"].get(telegram_id, "SAFE")

                # Store tier if provided
                if tier:
                    db["tiers"][telegram_id] = tier

                _save_db(db)

                # Log payment event (amount_cents=0 if not available in webhook)
                amount_cents = session.get("amount_total", 0)  # Stripe amount is in cents
                currency = session.get("currency", "usd")
                metrics.log_payment(telegram_id, amount_cents, currency)

    return jsonify({"ok": True})
