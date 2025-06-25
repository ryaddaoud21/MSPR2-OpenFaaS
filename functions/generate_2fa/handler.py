import pyotp
import qrcode
import io
import base64
import psycopg2
import json

def handle(event):
    if isinstance(event, str):
        try:
            data = json.loads(event)
        except Exception:
            return {"error": "Invalid JSON format"}
    elif isinstance(event, dict):
        data = event
    else:
        return {"error": "Unsupported input type"}

    username = data.get("username")
    if not username:
        return {"error": "Username required"}

    # 1. Générer un secret TOTP
    totp = pyotp.TOTP(pyotp.random_base32())
    secret = totp.secret

    # 2. Générer une URL OTP compatible avec Google Authenticator
    otp_uri = totp.provisioning_uri(name=username, issuer_name="MSPR-App")

    # 3. Générer le QR Code et encoder en base64
    qr = qrcode.make(otp_uri)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # 4. Connexion à PostgreSQL et vérification de l'utilisateur
    try:
        conn = psycopg2.connect(
            host="postgres.openfaas-fn.svc.cluster.local",
            dbname="mspr_db",
            user="mspr_user",
            password="motdepasse"
        )
        cur = conn.cursor()

        # Vérifie si l'utilisateur existe
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        result = cur.fetchone()

        if not result:
            return {"error": "User does not exist"}

        # Met à jour le champ MFA
        cur.execute("""
            UPDATE users SET mfa = %s WHERE username = %s
        """, (secret, username))
        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        return {"error": f"DB error: {str(e)}"}

    return {
        "message": "2FA secret generated and saved",
        "secret": secret,
        "qr_base64": qr_b64
    }
