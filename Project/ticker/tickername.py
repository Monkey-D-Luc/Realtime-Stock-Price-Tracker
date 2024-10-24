import pandas as pd
from yahooquery import Ticker
df = pd.read_excel('/content/drive/MyDrive/Colab Notebooks/filtered_tickers.xlsx')  
symbols = df['Ticker'].tolist()  
ticker = Ticker(symbols)
quote_data = ticker.quote_type 
companies = [quote_data.get(symbol, {}).get('shortName', 'N/A') for symbol in symbols]
df['Name'] = companies
df.to_excel('TickerName.xlsx', index=False)