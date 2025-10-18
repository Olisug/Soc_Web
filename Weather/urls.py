from django.urls import path
from . import views
from django.urls import path

app_name = 'Weather'

urlpatterns = [
    path('', views.show_my_apps, name='my_apps'),
    path('weather/', views.weather_app_view, name='weather-app'),
    path('coming_soon_1/', views.shop, name='shop'),
    path('coming_soon_2/', views.movieblog, name='movieblog')
]