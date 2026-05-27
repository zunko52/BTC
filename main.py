from flask import Flask
import os, time, hmac, hashlib, base64, requests, traceback

app = Flask(__name__)

API_KEY = os.getenv("BITGET_API_KEY")
SECRET_KEY = os.getenv("BITGET_SECRET_KEY")
PASSPHRASE = os.getenv("BITGET_PASSPHRASE")

BASE_URL = "https://api.bitget.com"

def make_sign(timestamp, method, request_path, body=""):
    message = timestamp + method + request_path + body
    signature = hmac.new(
        SECRET_KEY.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode()

@app.route("/")
def home():
    return "BOT RUNNING"

@app.route("/check")
def check():
    try:
        request_path = "/api/v2/mix/order/orders-pending?productType=usdt-futures"
        timestamp = str(int(time.time() * 1000))
        method = "GET"

        headers = {
            "ACCESS-KEY": API_KEY,
            "ACCESS-SIGN": make_sign(timestamp, method, request_path),
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": PASSPHRASE,
            "Content-Type": "application/json",
            "paptrading": "1"
        }

        response = requests.get(BASE_URL + request_path, headers=headers, timeout=10)
        return response.text

    except Exception as e:
        return "ERROR: " + str(e) + "\n\n" + traceback.format_exc()

app.run(host="0.0.0.0", port=10000)
