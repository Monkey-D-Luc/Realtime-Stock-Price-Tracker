
from django.contrib import admin
from django.urls import path
from .views import stock
from .views import search
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', search, name='search'),
]
