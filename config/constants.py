from datetime import datetime, timedelta

ENCTOKEN = "your_actual_enctoken_here"
USER_ID = " "

HEADERS = {
    "Authorization": f"enctoken {ENCTOKEN}"
}

TICKER_TOKENS = {
    "BAJAJFINSV": 4268801,
    # Add more tokens as needed
}

BASE_PATH = " "
START_DATE_DEFAULT = datetime(2019, 1, 1)
END_DATE_MASTER = datetime.now()
FETCH_DELTA = timedelta(days=1)
