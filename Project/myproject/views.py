from yahooquery import Ticker

symbols = 'fax'

tickers = Ticker(symbols)

# Retrieve each company's profile information
data = tickers.quote_type
print(data)