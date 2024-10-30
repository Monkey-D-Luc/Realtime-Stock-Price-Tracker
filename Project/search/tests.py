from django.test import TestCase
from yahooquery import Ticker
import pandas as pd
symbol = "TSLA" 
ticker = Ticker(symbol)
data = ticker.history(interval="1m", period="1d")
df = pd.DataFrame(data)
df.reset_index(inplace=True)
df['date'] = pd.to_datetime(df['date'])
df['hour'] = df['date'].dt.strftime('%H:%M')
print(df)
