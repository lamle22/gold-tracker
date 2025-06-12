import requests, sqlite3
from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app)
DB_FILE = 'gold_prices.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS gold_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            buy_price REAL,
            sell_price REAL
        );
    ''')
    conn.commit()
    conn.close()

def update_data():
    url = "https://sinhdien.com.vn/gia-vang-ajax-34255318"
    try:
        res = requests.get(url)
        res.raise_for_status()
        rows = res.json().get('rows', [])
        now = datetime.now().isoformat()
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        for row in rows:
            buy = float(row[1].replace(',', '').replace('.', ''))
            sell = float(row[2].replace(',', '').replace('.', ''))
            cur.execute("INSERT INTO gold_prices(timestamp,buy_price,sell_price) VALUES (?, ?, ?)",
                        (now, buy, sell))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error fetching:", e)

@app.route('/prices')
def get_prices():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT timestamp, buy_price, sell_price FROM gold_prices ORDER BY timestamp")
    result = cur.fetchall()
    conn.close()
    return jsonify([
        {"time": ts, "buy": bp, "sell": sp} for ts, bp, sp in result
    ])

if __name__ == "__main__":
    init_db()
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_data, 'interval', minutes=30)
    scheduler.start()
    app.run(host='0.0.0.0', port=5000)
