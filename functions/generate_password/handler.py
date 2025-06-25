import random
import string
import psycopg2
import json

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(random.choices(characters, k=length))
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in string.punctuation for c in password)):
            return password

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
        return {"error": "Username is required"}

    username = username.strip()

    # Génère le nouveau mot de passe
    new_password = generate_password()

    try:
        conn = psycopg2.connect(
            host="postgres",
            dbname="mspr_db",
            user="mspr_user",
            password="motdepasse"
        )
        cur = conn.cursor()

        # Vérifie que l'utilisateur existe
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if not user:
            cur.close()
            conn.close()
            return {"error": f"User '{username}' not found in database"}

        # Met à jour le mot de passe
        cur.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
        conn.commit()
        cur.close()
        conn.close()

        return {
            "message": f"Password updated for user '{username}'",
            "password": new_password
        }

    except Exception as e:
        return {"error": f"Database error: {str(e)}"}