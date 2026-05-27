from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "BOT RUNNING"

@app.route("/check")
def check():
    api = os.getenv("BITGET_API_KEY")
    secret = os.getenv("BITGET_SECRET_KEY")
    passphrase = os.getenv("BITGET_PASSPHRASE")

    return f"""
API_KEY: {'OK' if api else 'MISSING'}<br>
SECRET_KEY: {'OK' if secret else 'MISSING'}<br>
PASSPHRASE: {'OK' if passphrase else 'MISSING'}
"""

app.run(host="0.0.0.0", port=10000)

