from django.urls import path
from django.contrib import admin
from product.views import home_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
]
