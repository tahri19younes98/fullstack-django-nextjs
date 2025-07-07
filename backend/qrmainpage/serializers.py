from rest_framework import serializers
from .models import Restaurant, RestaurantImage

class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImage
        fields = ['id', 'image']

class RestaurantSerializer(serializers.ModelSerializer):
    images = RestaurantImageSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'
       # fields = ['id', 'name', 'facebook', 'instagram', 'tiktok', 'phone1', 'phone2', 'phone3', 'images']
