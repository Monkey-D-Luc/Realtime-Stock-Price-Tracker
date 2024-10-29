from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from yahooquery import Ticker
import pandas as pd
import os
excel_path = os.path.join(settings.DATA_DIR,'TickerName.xlsx')
df = pd.read_excel(excel_path)
def index(request):
    return render(request, 'index.html')
def get_stock_name(symbol):
    row = df[df['Ticker'] == symbol]
    return row['Name'].values[0] if not row.empty else None
def search_stock(request):
    query = request.GET.get('q', '')
    if query:
        filtered_stocks = df[df['Name'].str.contains(query, case=False) | df['Ticker'].str.contains(query, case=False)]
        result = filtered_stocks[['Name', 'Ticker']].to_dict(orient='records')
    else:
        result = []
    return JsonResponse(result, safe=False)

def stock_detail(request, symbol):
    stock = Ticker(symbol)
    data = stock.history(period="1d", interval="1m").tail(1)
    profile = stock.summary_profile.get(symbol)
    if isinstance(profile, dict):
        description = profile.get("longBusinessSummary", "N/A")
    else:
        description = "N/A"
    if data.empty:
        return JsonResponse({'error': 'Không tìm thấy thông tin'}, status=404)
    name_row = df[df['Ticker'] == symbol]
    if not name_row.empty:
        name = name_row['Name'].values[0]  
    else:
        name = "N/A"  
    close_price = data["close"].values[0]
    return render(request, 'stock.html', {'name': name, 'close': close_price, 'symbol': symbol, 'profile':description})

