from yahooquery import Ticker
import pandas as pd

def get_monthly_data(symbol, year, month):
    # Tạo khoảng thời gian đầu và cuối cho tháng cụ thể
    start_date = f"{year}-{month:02d}-01"
    if month == 12:
        end_date = f"{year + 1}-01-01"
    else:
        end_date = f"{year}-{month + 1:02d}-01"
    
    # Lấy dữ liệu lịch sử trong khoảng thời gian
    stock = Ticker(symbol)
    data = stock.history(start=start_date, end=end_date, interval="1d")
    
    # Chuyển đổi dữ liệu thành DataFrame
    if isinstance(data, pd.DataFrame):
        data = data.reset_index()
        
        # Lọc dữ liệu theo tháng và năm mong muốn
        data['date'] = pd.to_datetime(data['date'])
        data = data[(data['date'].dt.year == year) & (data['date'].dt.month == month)]
        
        return data[['date', 'open', 'high', 'low', 'close', 'volume']]
    else:
        print("Không thể lấy dữ liệu.")
        return None

# Ví dụ sử dụng
symbol = 'AAPL'
year = 2023
month = 7
monthly_data = get_monthly_data(symbol, year, month)
print(monthly_data)
