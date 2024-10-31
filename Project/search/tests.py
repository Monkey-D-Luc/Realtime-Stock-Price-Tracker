import pandas as pd
from yahooquery import Ticker

symbol = "TSLA"
ticker = Ticker(symbol)
data = ticker.history(interval="1d", period="1mo")
data = data.reset_index()
df = pd.DataFrame(data)
df['date'] = df['date'].astype(str)
df = df[df['date'].str.len() <= 10]
df['date'] = pd.to_datetime(df['date'])



print("Kiểu dữ liệu của các cột trong data:")
print(data.dtypes)

print("\nKiểu dữ liệu của các cột trong df:")
print(df.dtypes)