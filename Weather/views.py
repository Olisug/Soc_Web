from django.shortcuts import render
from Weather.forms import WeatherForm
from Weather.services import WeatherAPIClient
from Weather.models import Apps


def show_my_apps(request):
    all_apps = Apps.objects.all()
    return render(request,
                  'users/my_apps.html',
                  {'apps': all_apps})


def weather_app_view(request):
    form = WeatherForm()
    weather_data = None
    error = None
    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_client = WeatherAPIClient()
            weather_data = weather_client.get_weather(city)
    context = {'form': form,
               'weather_data': weather_data, 
               'error': error}
    return render(request, 'apps/weather_app.html', context)


def movieblog(request):
    return render(request,
                  'apps/coming_soon.html')


def shop(request):
    return render(request,
                  'apps/coming_soon.html')