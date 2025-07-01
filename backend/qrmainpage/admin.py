from django.contrib import admin

# Register your models here.

from .models import Restaurant, RestaurantImage

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'facebook', 'instagram', 'tiktok', 'phone1', 'phone2', 'phone3')
    search_fields = ('name', 'facebook', 'instagram', 'tiktok')

@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'image')
    search_fields = ('restaurant__name',)
    list_filter = ('restaurant',)
    