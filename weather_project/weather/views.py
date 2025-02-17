import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import WeatherSearch
from .serializers import WeatherSerializer

# OpenWeatherMap API Key (Replace with your own API key)
OPENWEATHER_API_KEY = "231fd0c6a0520bdf81e7874bfecb363f"

@api_view(['GET'])
def get_weather(request, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        # Save search history in database
        weather_search = WeatherSearch.objects.create(city=city)
        serializer = WeatherSerializer(weather_search)

        return Response({
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "timestamp": serializer.data["timestamp"]
        })
    else:
        return Response({"error": "City not found"}, status=404)

import requests
from django.shortcuts import render

def weather_view(request):
    city = request.GET.get('city', 'Kathmandu')  # Default to Kathmandu if no city is provided
    api_key = "231fd0c6a0520bdf81e7874bfecb363f"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:  # Successful API response
        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "icon": data["weather"][0]["icon"]
        }
    else:
        weather_data = {"error": "City not found!"}

    return render(request, "weather.html", {"weather": weather_data})
