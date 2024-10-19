
from django.shortcuts import render
import requests

API_KEY = 'po3cEYFATFj3Qm0POhPDK_E1scpkwFnC'

def stock(request):
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
        
        return render(request, 'stock_result.html', {'stock_info': stock_info})
    
    return render(request, 'stock.html')

# Hàm để gửi yêu cầu tới Alpha Vantage API
def search(request):
    if request.method == 'GET':
        symbol = request.GET.get('symbol')
        api_key = '39Y4RULMSAX9T0LI'  # API key của bạn
        
        if symbol:
            url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey={api_key}"
            response = requests.get(url)
            data = response.json()

            results = []
            if "bestMatches" in data:
                for match in data['bestMatches']:
                    # Chuyển đổi và ghi đè trực tiếp
                    for key in list(match.keys()):
                        new_key = key.replace('.', '_').replace(' ','')
                        match[new_key] = match.pop(key)  # Ghi đè bằng cách đổi tên key
                    
                    results.append(match)

                context = {
                    'results': results,
                    'symbol': symbol
                }
            else:
                context = {
                    'error': 'No results found.',
                    'symbol': symbol
                }
        else:
            context = {
                'error': 'Please enter a symbol to search.'
            }

        return render(request, 'search.html', context)

