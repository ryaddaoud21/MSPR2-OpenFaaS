import psycopg2
import json
import time
import bcrypt

def handle(event):
    # 1. Charger les données JSON
    if isinstance(event, str):
        try:
            data = json.loads(event)
        except Exception:
            return {"error": "Invalid JSON format"}
    elif isinstance(event, dict):
        data = event
    else:
        return {"error": "Unsupported input type"}

    # 2. Extraire et valider les champs
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    mfa = data.get("mfa", "").strip()

    if not username or not password:
        return {"error": "Username and password are required"}
    if len(username) > 50 or len(password) > 100:
        return {"error": "Input too long"}

    # 3. Connexion DB
    try:
        conn = psycopg2.connect(
            host="postgres",
            dbname="mspr_db",
            user="mspr_user",
            password="motdepasse"
        )
        cur = conn.cursor()

        # 4. Vérifier si le username existe déjà
        cur.execute("SELECT 1 FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return {"error": "⚠️ Username already exists"}

        # 5. Hacher le mot de passe
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # 6. Infos supplémentaires
        gendate = int(time.time())
        expired = False

        # 7. Insertion sécurisée
        cur.execute("""
            INSERT INTO users (username, password, mfa, gendate, expired)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, hashed_password, mfa, gendate, expired))
        conn.commit()
        cur.close()
        conn.close()

        return {"status": "✅ User created securely"}

    except Exception as e:
        return {"error": "DB error: " + str(e)}
