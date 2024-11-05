import yahooquery as yq

# Gọi phương thức get_trending để lấy dữ liệu
trending_data = yq.get_trending()
symbols = [item['symbol'] for item in trending_data['quotes']]
    
    # In ra danh sách các mã cổ phiếu
print("Danh sách các mã cổ phiếu đang thịnh hành:")
for symbol in symbols:
    print(symbol)