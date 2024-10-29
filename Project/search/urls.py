from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  
    path('search/', views.search_stock, name='search_stock'),
    path('<str:symbol>/profile/', views.stock_detail, name='stock_detail'),
    #path('chart', views.chart_view, name='chart'),
    #path('historical-data', views.historical_data_view, name='historical-data'),
    #path('analysis', views.analysis_view, name='analysis'),
]

