from django.test import TestCase
from yahooquery import Ticker

# Khởi tạo cổ phiếu với ký hiệu (symbol) bạn muốn
symbol = "TSLA"  # thay "AAPL" bằng mã cổ phiếu của bạn
ticker = Ticker(symbol)

# Lấy dữ liệu giá cổ phiếu trong 1 phút gần nhất
data = ticker.history(interval="1m", period="1d")
print(data)
