import requests
import csv
from datetime import datetime
from bs4 import BeautifulSoup

CSV_FILE = "/data/gold_prices.csv"
URL = "https://sinhdien.com.vn/gia-vang-ajax-34255318"

def fetch_data():
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 3:
                try:
                    gia_mua = int(cells[1].text.strip().replace('.', '').replace(',', ''))
                    gia_ban = int(cells[2].text.strip().replace('.', '').replace(',', ''))
                    break
                except ValueError:
                    continue
        else:
            print("Không tìm thấy dữ liệu phù hợp.")
            return

        timestamp = datetime.now().isoformat()

        with open(CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, gia_mua, gia_ban])
        print(f"✔ Dữ liệu đã lưu: {timestamp}, {gia_mua}, {gia_ban}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    fetch_data()
