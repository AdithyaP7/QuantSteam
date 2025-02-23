import os
import requests
import json
from dotenv import load_dotenv
from kafka import KafkaProducer
import time

load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

KAFKA_TOPIC = "stock_data"
KAFKA_BROKER = "localhost:9091"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_stock_data(symbol):
    """Fetch real-time stock data from Alpha Vantage API."""
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "1min",
        "apikey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "Time Series (1min)" in data:
        latest_time = list(data["Time Series (1min)"].keys())[0]
        stock_info = data["Time Series (1min)"][latest_time]
        return {
            "symbol": symbol,
            "timestamp": latest_time,
            "open": stock_info["1. open"],
            "high": stock_info["2. high"],
            "low": stock_info["3. low"],
            "close": stock_info["4. close"],
            "volume": stock_info["5. volume"]
        }
    else:
        print(f"Error fetching data for {symbol}: {data.get('Note', 'Unknown error')}")
        return None

def send_to_kafka(symbol):
    """Fetch data and send it to Kafka."""
    stock_data = fetch_stock_data(symbol)
    if stock_data:
        producer.send(KAFKA_TOPIC, value=stock_data)
        producer.flush()
        print(f"Sent to Kafka: {stock_data}")

if __name__ == "__main__":
    stock_symbol = input("Enter stock symbol (e.g., AAPL, MSFT): ").upper()
    try:
        while True:
            send_to_kafka(stock_symbol)
            time.sleep(60)  
    except KeyboardInterrupt:
        print("Stopped producer.")
