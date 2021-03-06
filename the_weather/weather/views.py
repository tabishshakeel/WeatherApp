import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityFrom


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4bc514d5f36931e12234ef7d38b3700c'
    if request.method == 'POST':
        form = CityFrom(request.POST)
        form.save()

    form = CityFrom()

    cities = City.objects.all()
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'id': city.id,
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/weather.html', context)


def delete(request, id):
    if request.method == 'POST':
        City.objects.filter(id=id).delete()

    return redirect('/')
