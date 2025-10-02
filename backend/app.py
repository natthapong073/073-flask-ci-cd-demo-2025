from flask import Flask, jsonify
import os
import psycopg2
import redis

app = Flask(__name__)

# Database config (ใช้ค่าจาก docker-compose หรือ .env)
DB_NAME = os.getenv("POSTGRES_DB", "mydb")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "pass")
DB_HOST = os.getenv("DB_HOST", "db")  # service name ของ postgres ใน docker-compose
DB_PORT = os.getenv("DB_PORT", "5432")

# Redis config
REDIS_HOST = os.getenv("REDIS_HOST", "redis")  # service name ของ redis ใน docker-compose
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


@app.route("/")
def hello():
    return jsonify({
        "message": "Hello World!",
        "status": "running"
    })


@app.route("/health")
def health():
    status = {"status": "healthy"}

    # Check database connection
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.close()
        status["database"] = "connected"
    except Exception as e:
        status["database"] = f"error: {str(e)}"

    # Check redis connection
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        r.ping()
        status["redis"] = "connected"
    except Exception as e:
        status["redis"] = f"error: {str(e)}"

    return jsonify(status)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
