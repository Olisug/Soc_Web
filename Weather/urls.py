from django.urls import path
from . import views

app_name = 'Weather'

urlpatterns = [
    path('api/weather/', views.show_weather, name='show_weather'),
]
