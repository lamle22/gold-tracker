from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Kết nối DB từ biến môi trường
conn = psycopg2.connect(
    host=os.environ['DB_HOST'],
    database=os.environ['DB_NAME'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
    port=os.environ['DB_PORT']
)
cur = conn.cursor()

# Tạo bảng nếu chưa có
cur.execute("""
    CREATE TABLE IF NOT EXISTS gold_prices (
        id SERIAL PRIMARY KEY,
        date DATE,
        price NUMERIC
    )
""")
conn.commit()

@app.route("/add", methods=["POST"])
def add_price():
    data = request.json
    cur.execute("INSERT INTO gold_prices (date, price) VALUES (%s, %s)",
                (data["date"], data["price"]))
    conn.commit()
    return jsonify({"status": "success"}), 201

@app.route("/prices", methods=["GET"])
def get_prices():
    cur.execute("SELECT * FROM gold_prices")
    rows = cur.fetchall()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
