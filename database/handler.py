import psycopg2
import os
import time

def handle(event):
    data = event if isinstance(event, dict) else {}
    username = data.get("username")
    password = data.get("password")
    mfa = data.get("mfa", "")
    gendate = int(time.time())
    expired = False

    conn = psycopg2.connect(
        host="postgres",
        dbname="mspr_db",
        user="mspr_user",
        password="mspr_pass"
    )
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (username, password, mfa, gendate, expired)
        VALUES (%s, %s, %s, %s, %s)
    """, (username, password, mfa, gendate, expired))

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "User created successfully"}
