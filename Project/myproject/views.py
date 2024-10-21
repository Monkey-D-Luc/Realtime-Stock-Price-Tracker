from yahooquery import Ticker

symbols = 'CDTTW'

tickers = Ticker(symbols)

# Retrieve each company's profile information
data = tickers.asset_profile
print(data)