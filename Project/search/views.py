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
    profile = stock.summary_profile.get(symbol, {})
    description = profile.get("longBusinessSummary", "N/A")
    data = stock.history(interval="1d", period="1mo")
    data = data.reset_index() 
    mdata = pd.DataFrame(data)
    mdata['date'] = mdata['date'].astype(str)
    mdata = mdata[mdata['date'].str.len() <= 10]
    mdata['date'] = pd.to_datetime(mdata['date'])
    mdata['date'] = mdata['date'].dt.strftime('%d-%m-%Y')
    mdata = mdata.sort_values(by='date', ascending=False)
    compare = (mdata["close"].values[0]- mdata["close"].values[1]).round(2)
    percent= ((compare/mdata["close"].values[0].round(2))*100).round(2)
    name_row = df[df['Ticker'] == symbol]
    name = name_row['Name'].values[0] if not name_row.empty else "N/A"
    close_price = mdata["close"].values[0].round(2)
    return name, close_price, symbol, description,compare,percent,mdata

def stock_profile(request, symbol):
    name, close_price, symbol, description,compare,percent,_ = get_stock_data(symbol)
    if name is None:
        return JsonResponse({'error': 'Không tìm thấy thông tin'}, status=404)
    return render(request, 'profile.html', {
        'name': name,
        'close': close_price,
        'symbol': symbol,
        'profile': description,
        'compare':compare,
        'percent':percent
    })
    
def historical(request, symbol):
    name, close_price, symbol, _,compare,percent,mdata = get_stock_data(symbol)
    mdata[['open', 'high', 'low', 'close']] = mdata[['open', 'high', 'low', 'close']].round(2)
    history_data = mdata[['date', 'open', 'high', 'low', 'close', 'volume']].to_dict(orient='records')
    return render(request, 'history.html', {
        'name': name,
        'symbol': symbol,
        'history_data': history_data,
        'close': close_price,
        'compare':compare,
        'percent':percent
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
    name, close_price, symbol, _,compare,percent,_ = get_stock_data(symbol)
    context = {
        'name': name,
        'symbol': symbol,
        'close': close_price,
        'timestamps': json.dumps(hour),
        'close_prices': json.dumps(close_list),
        'compare':compare,
        'percent':percent,
    }
    return render(request, 'chart.html', context)