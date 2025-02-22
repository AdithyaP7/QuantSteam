import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

BASE_URL = "https://www.alphavantage.co/query"

def fetch_real_time_stock_price(symbol):
    """Fetch real-time stock data for a given symbol."""
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "1min", 
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if "Time Series (1min)" in data:
            latest_time = list(data["Time Series (1min)"].keys())[0]
            latest_data = data["Time Series (1min)"][latest_time]
            print(f"Latest data for {symbol} at {latest_time}: {latest_data}")
            return latest_data
        else:
            print("API limit reached or invalid symbol.")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    stock_symbol = input("Enter stock symbol (e.g., AAPL, MSFT): ")
    fetch_real_time_stock_price(stock_symbol.upper())
