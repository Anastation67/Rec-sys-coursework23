
from django.contrib import admin
from django.urls import re_path
from . import views
from product.views import home_view
from django.urls import path



urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/',home_view, name='home'),
    path('about/', views.about),
]
