FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
COPY ./data/gold_prices.csv /data/gold_prices.csv  # 👈 Dòng này là quan trọng

CMD ["python", "app.py"]
