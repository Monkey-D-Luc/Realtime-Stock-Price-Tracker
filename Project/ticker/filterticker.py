import pandas as pd
from yahooquery import Ticker

df = pd.read_excel("/content/drive/MyDrive/Colab Notebooks/tickers.xlsx")
symbols = df['Ticker'].tolist()
tickers = Ticker(symbols)
profiles = tickers.asset_profile
valid_tickers = [symbol for symbol, profile in profiles.items() if profile and 'longBusinessSummary' in profile]
filtered_df = pd.DataFrame(valid_tickers, columns=["Ticker"])
filtered_df.to_excel("filtered_tickers.xlsx", index=False)
print("Danh sách mã ticker hợp lệ đã được lưu vào file filtered_tickers.xlsx")