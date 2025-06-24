import requests
import time
from config.constants import HEADERS

def fetch_historical_data(token, user_id, start, end, session=None):
    session = session or requests.Session()
    url = f"https://kite.zerodha.com/oms/instruments/historical/{token}/minute"
    params = {
        "user_id": user_id,
        "oi": 1,
        "from": start.strftime("%Y-%m-%d"),
        "to": end.strftime("%Y-%m-%d")
    }

    try:
        response = session.get(url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("data", {}).get("candles", [])
    except Exception as e:
        print(f"⚠️ Error fetching data: {e}. Retrying in 5 seconds...")
        time.sleep(5)
        return []
