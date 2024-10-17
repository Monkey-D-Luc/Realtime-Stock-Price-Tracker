from django.urls import path
from .views import search_stock

urlpatterns = [
    path('search/', search_stock, name='search_stock'),
]
