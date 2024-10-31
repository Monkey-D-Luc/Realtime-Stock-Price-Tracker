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

def get_stock_data(symbol):
    stock = Ticker(symbol)
    data = stock.history(period="1d", interval="1m").tail(1)
    profile = stock.summary_profile.get(symbol, {})
    description = profile.get("longBusinessSummary", "N/A")
    if data.empty:
        return None, "Không tìm thấy thông tin", None, None
    name_row = df[df['Ticker'] == symbol]
    name = name_row['Name'].values[0] if not name_row.empty else "N/A"
    close_price = data["close"].values[0].round(2)
    return name, close_price, symbol, description

def stock_profile(request, symbol):
    name, close_price, symbol, description = get_stock_data(symbol)
    if name is None:
        return JsonResponse({'error': 'Không tìm thấy thông tin'}, status=404)
    return render(request, 'profile.html', {
        'name': name,
        'close': close_price,
        'symbol': symbol,
        'profile': description
    })
    
def historical(request, symbol):
    stock = Ticker(symbol)
    data = stock.history(period="1mo", interval="1d")
    if data.empty:
        return JsonResponse({'error': 'Không tìm thấy thông tin'}, status=404)
    data.reset_index(inplace=True)  
    data = data.sort_values(by='date', ascending=False)
    data[['open', 'high', 'low', 'close']] = data[['open', 'high', 'low', 'close']].round(2)
    name, close_price, symbol, _ = get_stock_data(symbol)
    history_data = data[['date', 'open', 'high', 'low', 'close', 'volume']].to_dict(orient='records')
    return render(request, 'history.html', {
        'name': name,
        'symbol': symbol,
        'history_data': history_data,
        'close': close_price
    })
    
def chart_view(request, symbol):
    stock = Ticker(symbol)
    data = stock.history(period="1d", interval="1m")
    if data.empty:
        return render(request, 'chart.html', {'error': 'Không tìm thấy dữ liệu'})
    daf = pd.DataFrame(data)
    daf.reset_index(inplace=True)
    daf['date'] = pd.to_datetime(daf['date'])
    daf['hour'] = daf['date'].dt.strftime('%H:%M')
    close_list = data["close"].tolist()
    hour = daf['hour'].tolist()
    name, close_price, symbol, _ = get_stock_data(symbol)
    context = {
        'name': name,
        'symbol': symbol,
        'close': close_price,
        'timestamps': json.dumps(hour),
        'close_prices': json.dumps(close_list),
    }
    return render(request, 'chart.html', context)