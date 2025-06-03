from django.contrib import admin

from .models import Domain,Fournisseur,Fr_Dom

# Register your models here.
admin.site.register(Fournisseur)

admin.site.register(Domain)

admin.site.register(Fr_Dom)