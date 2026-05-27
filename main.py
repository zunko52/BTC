from flask import Flask
import os, time, hmac, hashlib, base64, requests, traceback

app = Flask(__name__)

API_KEY = os.getenv("BITGET_API_KEY", "").strip()
SECRET_KEY = os.getenv("BITGET_SECRET_KEY", "").strip()
PASSPHRASE = os.getenv("BITGET_PASSPHRASE", "").strip()

BASE_URL = "https://api.bitget.com"

def get_timestamp():
    return str(int(time.time() * 1000))

def to_query_no_encode(params):
    items = [(key, value) for key, value in params.items()]
    items.sort(key=lambda x: x[0])
    return "?" + "&".join([f"{k}={v}" for k, v in items])

def pre_hash(timestamp, method, request_path, body):
    return str(timestamp) + method.upper() + request_path + body

def sign(message, secret_key):
    mac = hmac.new(
        bytes(secret_key, encoding="utf8"),
        bytes(message, encoding="utf-8"),
        digestmod="sha256"
    )
    return base64.b64encode(mac.digest()).decode()

@app.route("/")
def home():
    return "BOT RUNNING"

@app.route("/check")
def check():
    try:
        timestamp = get_timestamp()
        method = "GET"
        body = ""

        request_path = "/api/v2/mix/account/account"
        params = {
            "marginCoin": "USDT",
            "symbol": "BTCUSDT"
        }

        full_request_path = request_path + to_query_no_encode(params)

        signature = sign(
            pre_hash(timestamp, method, full_request_path, body),
            SECRET_KEY
        )

        headers = {
            "ACCESS-KEY": API_KEY,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": PASSPHRASE,
            "Content-Type": "application/json",
            "paptrading": "1"
        }

        url = BASE_URL + full_request_path
        response = requests.get(url, headers=headers, timeout=10)

        return response.text

    except Exception as e:
        return "ERROR: " + str(e) + "\n\n" + traceback.format_exc()

app.run(host="0.0.0.0", port=10000)
