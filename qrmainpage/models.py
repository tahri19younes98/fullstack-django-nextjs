from django.db import models

# Create your models here.

class Restaurant(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True,unique=True)
    name = models.CharField(max_length=100)
    
    facebook = models.CharField(max_length=100, blank=True)
    facebookUser = models.CharField(max_length=100, blank=True)
    
    instagram = models.CharField(max_length=100, blank=True)
    instagramUser = models.CharField(max_length=100, blank=True)
    
    tiktok = models.CharField(max_length=100, blank=True)
    tiktokUser = models.CharField(max_length=100, blank=True)
    
    phone1 = models.CharField(max_length=20, blank=True)
    phone2 = models.CharField(max_length=20, blank=True)
    phone3 = models.CharField(max_length=20, blank=True)
    

    def __str__(self):
        return self.name


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='restaurant_images/')

    def __str__(self):
        return f"{self.restaurant.name} - Image {self.id}"