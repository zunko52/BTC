from flask import Flask
import os
import traceback

from bitget.v2.mix.account_api import AccountApi

app = Flask(__name__)

API_KEY = os.getenv("BITGET_API_KEY", "").strip()
SECRET_KEY = os.getenv("BITGET_SECRET_KEY", "").strip()
PASSPHRASE = os.getenv("BITGET_PASSPHRASE", "").strip()

@app.route("/")
def home():
    return "BOT RUNNING"

@app.route("/check")
def check():
    try:
        api = AccountApi(API_KEY, SECRET_KEY, PASSPHRASE)

        params = {
            "symbol": "BTCUSDT",
            "marginCoin": "USDT"
        }

        result = api.account(params)
        return str(result)

    except Exception as e:
        return "ERROR: " + str(e) + "\n\n" + traceback.format_exc()

app.run(host="0.0.0.0", port=10000)
