from yahooquery import Ticker
import pandas as pd


# Ví dụ sử dụng
symbol = 'AAPL'
year = 2024
month = 11
stock = Ticker(symbol)
data = stock.history(  period="1mo", interval="1d")
print(data)
