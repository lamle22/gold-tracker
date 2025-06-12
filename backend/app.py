import requests
import re
import psycopg2
from datetime import datetime

# Kết nối PostgreSQL
conn = psycopg2.connect(
    host="localhost",  # hoặc 'db' nếu dùng Docker
    database="gold_db",
    user="postgres",
    password="postgres"
)
cur = conn.cursor()

# Lấy HTML từ trang web
url = "https://sinhdien.com.vn/gia-vang-ajax-34255318"
res = requests.get(url)
html = res.text

# Lấy thời gian cập nhật
match_time = re.search(r'Cập nhật lúc: ([\d: ]+\d{2}/\d{2}/\d{4})', html)
if match_time:
    updated_at = datetime.strptime(match_time.group(1), "%H:%M %d/%m/%Y")
else:
    updated_at = datetime.now()

# Danh sách loại vàng
items = {
    "Nhẫn tròn 999": None,
    "Nhẫn vỉ 999,9": None,
    "Vàng 18K": None,
    "Vàng 610": None,
    "Vàng 14K": None,
    "Vàng 10K": None,
    "Bạc": None,
    "Thần tài": None
}

for name in items.keys():
    pattern = fr'<tr><td>{re.escape(name)}</td><td>([\d,]+)</td><td>([\d,]+)</td></tr>'
    match = re.search(pattern, html)
    if match:
        buy = float(match.group(1).replace(',', ''))
        sell = float(match.group(2).replace(',', ''))
        items[name] = (buy, sell)
        
        # Ghi vào DB
        cur.execute(
            "INSERT INTO gold_prices (name, buy_price, sell_price, updated_at) VALUES (%s, %s, %s, %s)",
            (name, buy, sell, updated_at)
        )
        print(f"{name} - Mua vào: {buy} | Bán ra: {sell}")
    else:
        print(f"Không tìm thấy {name}")

conn.commit()
cur.close()
conn.close()
