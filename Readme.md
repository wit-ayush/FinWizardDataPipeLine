
# 🧠 FinWizard Data Pipeline

A modular and extensible data engineering pipeline to fetch, process, and store historical market data for equities and indices — designed with high-frequency, low-latency financial applications in mind.

---

## 🚀 Overview

This project implements a **production-grade ETL pipeline** in Python to collect historical minute-level data from Zerodha's Kite API, enrich it with technical indicators, and store it in Parquet format for high-performance analytics and backtesting.

It mimics the architecture often seen in quantitative trading and research systems, focusing on **scalability, modularity, and precision**.

---

## 📁 Project Structure

```
FINWIZARDDATAPIPELINE/
│
├── config/
│   └── constants.py         # API keys, date config, storage paths
│
├── data/                    # Output directory for processed data
│   ├── BAJAJFINSV/
│   └── dummy/
│
├── utils/
│   ├── data_handler.py      # ETL orchestrator
│   ├── indicators.py        # Technical indicators (RSI, MACD, etc.)
│   └── kite_api.py          # Historical data wrapper for Kite API
│
├── main.py                  # Entry point (optional)
├── requirements.txt         # Project dependencies
└── .gitignore
```

---

## 🧩 Core Features

- ✅ **Historical data ingestion** using Zerodha Kite HTTP API
- 📈 **On-the-fly technical computation**: RSI, MACD, ATR, Bollinger Bands, VWAP, EMAs
- 💾 **Parquet-based storage** for fast columnar queries
- 🔁 **Incremental updates**: avoids redundant downloads
- 🔐 Designed with **thread-safe file operations**, but currently runs sequentially

---

## ⚙️ How It Works

1. **Pull minute-level OHLCV+OI data** from the Kite API
2. **Calculate indicators** on-the-fly using rolling/statistical methods
3. **Write to Parquet files**, chunked by date range

---

## 📊 Output Format

Sample columns:

| date       | time     | open  | high  | low   | close | RSI   | MACD  | VWAP  |
|------------|----------|-------|-------|-------|-------|--------|--------|--------|
| 2024-06-01 | 09:15:00 | 715.0 | 716.5 | 714.2 | 716.0 | 52.40 | 1.23  | 715.7  |

Data is clean, enriched, and optimized for downstream consumption by:

- Backtesters
- ML pipelines
- Trading signal engines
- Exploratory dashboards

---

## ✅ Usage

### 1. Install requirements

```bash
pip install -r requirements.txt
```

### 2. Configure your settings in `config/constants.py`

```python
BASE_PATH = './data/'
USER_ID = 'XXXXXX'
HEADERS = {
    "Authorization": "enctoken XXXXXXXXX",
    "X-Kite-Version": "3"
}
START_DATE_DEFAULT = datetime(2024, 6, 1)
END_DATE_MASTER = datetime(2024, 6, 25)
```

### 3. Run the pipeline

```python
from utils.data_handler import update_index_data

update_index_data(index_name="BAJAJFINSV", token=123456)
```

---

## 📌 Why This Project?

- 🧠 Demonstrates fluency in **financial data structures** and **timeseries processing**
- 📦 Focuses on **efficient storage** and scalable design
- 🔍 Highlights capability in **building real-world data infrastructure**
- 🧩 Built to plug directly into backtesters, dashboards, or strategy layers

---

## 🛠️ Possible Extensions

- [ ] Add CLI or scheduler for automation
- [ ] Extend to live streaming mode with WebSockets
- [ ] Add retry logic, failover, and metadata tracking
- [ ] Build a web dashboard for visual insights
- [ ] Introduce unit tests and coverage reports

---

## 🧾 License

MIT License. Built for educational and analytical purposes.

---

## 🙋 Reach Out

Happy to explain design decisions, use cases, and potential improvements.
