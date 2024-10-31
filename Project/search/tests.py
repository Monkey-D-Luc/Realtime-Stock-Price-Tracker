from django.test import TestCase
from yahooquery import Ticker
import pandas as pd
symbol = "TSLA" 
ticker = Ticker(symbol)
data = ticker.history(interval="1d", period="1mo")
data = data.sort_values(by='date', ascending=False)
compare = (data["close"].values[0]- data["close"].values[1]).round(2)
percent= ((compare/data["close"].values[0].round(2))*100).round(2)
print(compare)
print(percent,"%")