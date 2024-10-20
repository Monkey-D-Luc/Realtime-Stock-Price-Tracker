
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.search, name='search'),
    path('<str:symbol>/', views.stock_detail, name='stock_detail'),
]
