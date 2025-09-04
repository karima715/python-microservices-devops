import os
import json
import time
from typing import Optional
from flask import Flask, jsonify, request
import psycopg2
import requests

def get_db_conn():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "db"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        user=os.getenv("POSTGRES_USER", "appuser"),
        password=os.getenv("POSTGRES_PASSWORD", "apppass"),
        dbname=os.getenv("POSTGRES_DB", "appdb"),
    )

def init_db():
    ddl = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(ddl)
        conn.commit()

def make_app():
    app = Flask(__name__)
    app.config["LOGGER_URL"] = os.getenv("LOGGER_URL", "http://logger:9000/log")

    @app.before_first_request
    def _init():
        init_db()

    @app.get("/health")
    def health():
        try:
            with get_db_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1;")
                    _ = cur.fetchone()
            return jsonify({"status": "ok"}), 200
        except Exception as e:
            return jsonify({"status": "error", "detail": str(e)}), 500

    def log_event(event: str, extra: Optional[dict] = None):
        payload = {"event": event, "ts": time.time(), "extra": extra or {}}
        try:
            requests.post(app.config["LOGGER_URL"], json=payload, timeout=2)
        except Exception:
            # Don't break the request if logging fails
            pass

    @app.get("/api/data")
    def api_data():
        # Simple demo response + live count from DB
        try:
            with get_db_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) FROM users;")
                    (count,) = cur.fetchone()
        except Exception as e:
            count = None

        data = {
            "message": "Hello from backend",
            "db_user_count": count,
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        log_event("fetch_data", {"db_user_count": count})
        return jsonify(data), 200

    @app.post("/api/users")
    def create_user():
        body = request.get_json(force=True)
        name = (body or {}).get("name")
        email = (body or {}).get("email")
        if not name or not email:
            return jsonify({"error": "name and email are required"}), 400
        try:
            with get_db_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO users(name, email) VALUES(%s, %s) RETURNING id;",
                        (name, email),
                    )
                    (uid,) = cur.fetchone()
                conn.commit()
            log_event("create_user", {"id": uid, "email": email})
            return jsonify({"id": uid, "name": name, "email": email}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.get("/api/users")
    def list_users():
        try:
            with get_db_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, name, email, created_at FROM users ORDER BY id;")
                    rows = cur.fetchall()
            users = [
                {"id": r[0], "name": r[1], "email": r[2], "created_at": r[3].isoformat()}
                for r in rows
            ]
            return jsonify(users), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

# gunicorn will look for "app"
app = make_app()

if __name__ == "__main__":
    # dev-only
    app.run(host="0.0.0.0", port=5000, debug=True)
