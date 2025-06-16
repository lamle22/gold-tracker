# Sửa tên bảng: gold_prices -> gold_prices (giữ nguyên nếu bảng đúng)
cur.execute(
    "INSERT INTO gia_vang (name, buy_price, sell_price, updated_at) VALUES (%s, %s, %s, %s)",
    (name, buy, sell, updated_at)
)
