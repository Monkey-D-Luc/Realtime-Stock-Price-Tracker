from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='index'),  
    path('search/', views.search_stock, name='search_stock'),
    path('<str:symbol>/profile/', views.stock_profile, name='stock_detail'),
    path('<str:symbol>/chart/', views.chart_view, name='chart'),
    path('<str:symbol>/history/', views.historical, name='historical_data'),
    #path('<str:symbol>/analysis/', views.analysis_view, name='analysis'),
]

