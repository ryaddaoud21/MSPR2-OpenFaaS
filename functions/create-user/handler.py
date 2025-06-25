import psycopg2
import os
import time
import json

def handle(event):
    # Convertir la chaîne JSON en dictionnaire
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
    password = data.get("password")
    mfa = data.get("mfa", "")
    gendate = int(time.time())
    expired = False

    try:
        conn = psycopg2.connect(
            host="postgres",              # Assure-toi que le service s'appelle bien ainsi
            dbname="mspr_db",
            user="mspr_user",
            password="motdepasse"         # Remplace ici par ton vrai mot de passe
        )
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (username, password, mfa, gendate, expired)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, password, mfa, gendate, expired))
        conn.commit()
        cur.close()
        conn.close()

        return {"status": "User created"}
    except Exception as e:
        return {"error": str(e)}
