from flask import Flask, request
from discordwebhook import Discord
import yfinance as yf
import threading
import time

app = Flask(__name__)

currency_pair = "AUDJPY=X"
ticker = yf.Ticker(currency_pair)


def check_rate(rate_threshold):
    while True:
        data = ticker.history(period="1d")
        latest_rate = data["Close"].iloc[-1]
        rate = round(latest_rate, 4)
        if rate > rate_threshold:
            discord = Discord(url="https://discord.com/api/webhooks/1100010698320392202/j6kT02-yJchn-TqvoESDEPlsT5MFI4eviSpFIQo27nIvvbe1ZVVdzRvDykc4kRm1HyHf")
            discord.post(content=f"Rate {rate} exceeded the threshold {rate_threshold}!")
            break
        time.sleep(30)


@app.route('/check_rate', methods=['POST'])
def post_rate():
    rate_threshold = float(request.form['rate'])
    # Start checking rate in a separate thread
    # so that the Flask app can continue running
    # and handle other requests
    check_rate_thread = threading.Thread(target=check_rate, args=(rate_threshold,))
    check_rate_thread.start()
    return 'Rate check started.'

if __name__ == "__main__":
    app.run()
