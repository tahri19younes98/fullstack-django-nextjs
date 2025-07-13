from django.db import models

# Create your models here.
class Redirection(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True,unique=True)
    site = models.URLField(default="https://codeitdz.com")
    def __str__(self):
        return f"{self.id} => {self.site}"