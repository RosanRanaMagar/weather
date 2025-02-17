from rest_framework import serializers
from .models import WeatherSearch

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherSearch
        fields = '__all__'
