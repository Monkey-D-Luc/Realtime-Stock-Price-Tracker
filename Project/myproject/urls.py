
from django.contrib import admin
from django.urls import path
from .views import search_stock

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', search_stock, name='search_stock'),
]
