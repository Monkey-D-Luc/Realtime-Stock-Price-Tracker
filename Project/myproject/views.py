
from django.shortcuts import render
import requests

API_KEY = 'po3cEYFATFj3Qm0POhPDK_E1scpkwFnC'

def search_stock(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        date = '2024-10-16'  # Ví dụ ngày cố định, bạn có thể cho phép người dùng chọn ngày
        url = f'https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?apiKey={API_KEY}'
        
        response = requests.get(url)
        data = response.json()
        if 'results' in data:
            stock_info = next((stock for stock in data['results'] if stock['T'] == symbol), None)
        else:
            stock_info = None  
        
        return render(request, 'search_result.html', {'stock_info': stock_info})
    
    return render(request, 'search.html')
