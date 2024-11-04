import requests
import pandas as pd
url = "https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2024-10-18?adjusted=true&apiKey=po3cEYFATFj3Qm0POhPDK_E1scpkwFnC"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    tickers = []
    for stock in data.get("results", []):
        tickers.append(stock["T"])  # "T" là mã ticker
    df = pd.DataFrame(tickers, columns=["Ticker"])
    df.to_excel("tickers.xlsx", index=False)
    print("Danh sách mã ticker đã được lưu vào file tickers.xlsx")
