# keep_alive.py
from flask import Flask
from threading import Thread
import datetime

start_time = datetime.datetime.now()

app = Flask('')

@app.route('/')
def home():
    uptime = datetime.datetime.now() - start_time
    uptime_str = str(uptime).split('.')[0]  # bỏ phần microsecond cho gọn
    return f"✅ Webserver OK<br>Bot uptime: {uptime_str}"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    """Chạy Flask server song song, tránh block main thread"""
    t = Thread(target=run)
    t.start()
