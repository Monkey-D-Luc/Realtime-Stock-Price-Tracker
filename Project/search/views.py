from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
from yahooquery import Ticker
import yahooquery as yq
import json
import pandas as pd
import os
from datetime import datetime
excel_path = os.path.join(settings.DATA_DIR,'TickerName.xlsx')
df = pd.read_excel(excel_path)
def menu(request):
    trending_data = get_trending_data()
    return render(request, 'menu.html', {'trending_data': trending_data})

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
    cache_key = f"stock_data_{symbol}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    
    stock = Ticker(symbol)
    profile = stock.summary_profile.get(symbol, {})
    profile_details = [
        profile.get("longBusinessSummary", "N/A"),
        profile.get("address1", "N/A"),
        profile.get("city", "N/A"),
        profile.get("country", "N/A"),
        profile.get("phone", "N/A"),
        profile.get("website", "N/A"),
        profile.get("industry", "N/A"),
        profile.get("sector", "N/A"),
        profile.get("fullTimeEmployees", "N/A")
    ]
    data = stock.history(interval="1d", period="1mo")
    data = data.reset_index() 
    mdata = pd.DataFrame(data)
    mdata['date'] = mdata['date'].astype(str)
    mdata = mdata[mdata['date'].str.len() <= 10]
    mdata['date'] = pd.to_datetime(mdata['date'])
    mdata = mdata.sort_values(by='date', ascending=False)
    mdata['date'] = mdata['date'].dt.strftime('%d-%m-%Y')
    compare = (mdata["close"].values[0]- mdata["close"].values[1]).round(2)
    percent= ((compare/mdata["close"].values[0].round(2))*100).round(2)
    name_row = df[df['Ticker'] == symbol]
    name = name_row['Name'].values[0] if not name_row.empty else "N/A"
    close_price = mdata["close"].values[0].round(2)
    result = (name, close_price, symbol, profile_details, compare, percent, mdata)
    cache.set(cache_key, result, 3600)
    return result
def get_trending_data():
    cache_key = "trending_data"
    cached_trending_data = cache.get(cache_key)
    if cached_trending_data:
        return cached_trending_data
    trending_data = yq.get_trending()
    trending_results = []
    if trending_data and 'quotes' in trending_data:
        symbols = [item['symbol'] for item in trending_data['quotes'][:20]]
        stock = yq.Ticker(symbols)  
        data = stock.history(interval="1d", period="1mo")
        if isinstance(data, dict) and 'symbol' in data:
            data = pd.DataFrame(data)
        data = data.reset_index()
        data['date'] = data['date'].astype(str)
        data = data[data['date'].str.len() <= 10]
        data['date'] = pd.to_datetime(data['date'])
        data = data.sort_values(by='date', ascending=False)
        for symbol in symbols:
            if symbol in data['symbol'].values:
                stock_data = data[data['symbol'] == symbol]
                if not stock_data.empty:
                    latest_close = stock_data['close'].iloc[0]
                    previous_close = stock_data['close'].iloc[1]
                    
                    compare = (latest_close - previous_close).round(2)
                    percent = ((compare / previous_close) * 100).round(2)  
                    close_price = latest_close.round(2)
                    
                    trending_results.append({
                        'symbol': symbol,
                        'close_price': close_price,
                        'compare': compare,
                        'percent': percent
                    })
        cache.set(cache_key, trending_results, 3600)
    return trending_results


def stock_profile(request, symbol):
    name, close_price, symbol, profile_details,compare,percent,_ = get_stock_data(symbol)
    if name is None:
        return JsonResponse({'error': 'Không tìm thấy thông tin'}, status=404)
    return render(request, 'profile.html', {
        'name': name,
        'close': close_price,
        'symbol': symbol,
        'profile': profile_details[0],
        'address': profile_details[1],
        'city': profile_details[2],
        'country': profile_details[3],
        'phone': profile_details[4],
        'website': profile_details[5],
        'industry': profile_details[6],
        'sector': profile_details[7],
        'employees': profile_details[8],
        'compare':compare,
        'percent':percent
    })
    
def get_monthly_data(stock, year, month):
    start_date = f"{year}-{month:02d}-01"
    if month == 12:
        end_date = f"{year + 1}-01-01"
    else:
        end_date = f"{year}-{month + 1:02d}-01"
    
    data = stock.history(start=start_date, end=end_date, interval="1d")
    if isinstance(data, pd.DataFrame):
        data = data.reset_index()
        data['date'] = pd.to_datetime(data['date'])
        data = data[(data['date'].dt.year == year) & (data['date'].dt.month == month)]
        return data[['date', 'open', 'high', 'low', 'close', 'volume']].round(2).to_dict(orient='records')
    return []

def historical(request, symbol):
    name, close_price, symbol, _, compare, percent, mdata = get_stock_data(symbol)
    mdata[['open', 'high', 'low', 'close']] = mdata[['open', 'high', 'low', 'close']].round(2)
    current_history_data = mdata[['date', 'open', 'high', 'low', 'close', 'volume']].to_dict(orient='records')
    selected_month = int(request.GET.get('month', datetime.now().month))
    selected_year = int(request.GET.get('year', datetime.now().year))
    stock = Ticker(symbol)
    if selected_month == datetime.now().month and selected_year == datetime.now().year:
        history_data = current_history_data
    else:
        history_data = get_monthly_data(stock, selected_year, selected_month)

    year_range = range(2020, datetime.now().year + 1)
    month_range = range(1, 13) 
    return render(request, 'history.html', {
        'name': name,
        'symbol': symbol,
        'history_data': history_data,
        'close': close_price,
        'compare': compare,
        'percent': percent,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'year_range': year_range,
        'month_range': month_range, 
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
    close_list = daf["close"].tolist()
    open_list=  daf['open'].tolist()
    high_list=daf['high'].tolist()
    low_list=daf['low'].to_list()
    volume= daf['volume'].tolist()
    hour = daf['hour'].tolist()
    name, close_price, symbol, _,compare,percent,_ = get_stock_data(symbol)
    context = {
        'name': name,
        'symbol': symbol,
        'close': close_price,
        'timestamps': json.dumps(hour),
        'compare':compare,
        'percent':percent,
        'low_prices': json.dumps(low_list),
        'open_prices': json.dumps(open_list),
        'high_prices': json.dumps(high_list),
        'volume': json.dumps(volume),
        'close_prices': json.dumps(close_list),
    }
    return render(request, 'chart.html', context)