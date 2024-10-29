from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  
    path('search/', views.search_stock, name='search_stock'),
    path('<str:symbol>/', views.stock_detail, name='stock_detail'),
    #path('<str:symbol>/profile/',views.p)
]

