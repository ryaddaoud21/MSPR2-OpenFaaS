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
    password = data.get("password")

    if not username or not password:
        return {"error": "Missing username or password"}

    try:
        conn = psycopg2.connect(
            host="postgres",           # ou postgres.openfaas-fn.svc.cluster.local
            dbname="mspr_db",
            user="mspr_user",
            password="motdepasse"
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(*) FROM users
            WHERE username = %s AND password = %s
        """, (username, password))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result and result[0] > 0:
            return {"authenticated": True}
        else:
            return {"authenticated": False}

    except Exception as e:
        return {"error": str(e)}
