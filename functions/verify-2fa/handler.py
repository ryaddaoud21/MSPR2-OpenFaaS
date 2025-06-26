import pyotp
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
    token = data.get("token")

    if not username or not token:
        return {"error": "username and token are required"}

    try:
        conn = psycopg2.connect(
            host="postgres.openfaas-fn.svc.cluster.local",
            dbname="mspr_db",
            user="mspr_user",
            password="motdepasse"
        )
        cur = conn.cursor()

        cur.execute("SELECT mfa FROM users WHERE username = %s", (username,))
        result = cur.fetchone()

        if not result:
            return {"error": "User not found"}

        secret = result[0]
        totp = pyotp.TOTP(secret)

        if totp.verify(token):
            return {"message": "✅ Token is valid"}
        else:
            return {"error": "❌ Invalid token"}

    except Exception as e:
        return {"error": f"DB error: {str(e)}"}
