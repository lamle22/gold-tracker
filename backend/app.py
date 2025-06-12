from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Cho phép frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/prices")
def get_prices():
    conn = psycopg2.connect(
        host="db",         # ← nếu chạy trong docker
        database="gold_db",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT name, buy_price as buy, sell_price as sell, updated_at as time FROM gold_prices ORDER BY updated_at DESC LIMIT 100")
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
