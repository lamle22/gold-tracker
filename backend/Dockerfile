FROM python:3.10-slim

WORKDIR /app

COPY fetch_gold.py .
COPY cronjob /etc/cron.d/fetch-cron

RUN pip install requests beautifulsoup4 && \
    chmod 0644 /etc/cron.d/fetch-cron && \
    crontab /etc/cron.d/fetch-cron

CMD ["cron", "-f"]
