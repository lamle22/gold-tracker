import requests
import re
import csv
import os

url = "https://sinhdien.com.vn/gia-vang-ajax-34255318"
res = requests.get(url)
html = res.text

# Danh sách loại vàng
loai_vang = [
    "Nhẫn tròn 999",
    "Nhẫn vỉ 999,9",
    "Vàng 18K",
    "Vàng 610",
    "Vàng 14K",
    "Vàng 10K",
    "Bạc",
    "Thần tài"
]

# Dữ liệu
data = []

# Lấy thời gian cập nhật
match_time = re.search(r'Cập nhật lúc: ([\d: ]+\d{2}/\d{2}/\d{4})', html)
thoigian = match_time.group(1) if match_time else "Không rõ"
data.append(thoigian)

# Kiểm tra trùng lặp với dòng cuối
filename = "gia_vang.csv"
if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if lines:
            last_line = lines[-1].strip()
            if last_line.startswith(thoigian):
                print(f"Dữ liệu với thời gian '{thoigian}' đã tồn tại.")
                exit()

# Tiếp tục lấy dữ liệu vàng nếu không trùng
for ten in loai_vang:
    ten_escaped = re.escape(ten)
    match = re.search(rf'<tr><td>{ten_escaped}</td><td>([\d,]+)</td><td>([\d,]+)</td></tr>', html)
    if match:
        mua = match.group(1)
        ban = match.group(2)
    else:
        mua = ban = "Không tìm thấy"
    data.extend([mua, ban])

# Ghi vào CSV
with open(filename, mode="a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(data)

print(f"Đã cập nhật dữ liệu mới {filename}")
