from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from yahooquery import Ticker
import json
import pandas as pd
import os
excel_path = os.path.join(settings.DATA_DIR,'TickerName.xlsx')
df = pd.read_excel(excel_path)
def menu(request):
    return render(request, 'menu.html')
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

def stock_profile(request, symbol):
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
    return render(request, 'profile.html', {'name': name, 'close': close_price, 'symbol': symbol, 'profile':description})

def historical(request, symbol):
    stock = Ticker(symbol)
    data = stock.history(period="1mo", interval="1d")
    if data.empty:
        return JsonResponse({'error': 'Không tìm thấy thông tin'}, status=404)
    data.reset_index(inplace=True)  
    name_row = df[df['Ticker'] == symbol]
    if not name_row.empty:
        name = name_row['Name'].values[0]
    else:
        name = "N/A"
    history_data = data[['date', 'open', 'high', 'low', 'close', 'volume']].to_dict(orient='records')
    return render(request, 'history.html', {
        'name': name,
        'symbol': symbol,
        'history_data': history_data
    })
def chart_view(request, symbol):
    stock = Ticker(symbol)
    data = stock.history(period="1d", interval="1m")
    if data.empty:
        return render(request, 'chart.html', {'error': 'Không tìm thấy dữ liệu'})
    df = pd.DataFrame(data)
    df.reset_index(inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df['hour'] = df['date'].dt.strftime('%H:%M')
    close_prices = data["close"].tolist()
    hour= df['hour'].tolist()
    context = {
        'symbol': symbol,
        'timestamps': json.dumps(hour),
        'close_prices': json.dumps(close_prices),
    }
    return render(request, 'chart.html', context)