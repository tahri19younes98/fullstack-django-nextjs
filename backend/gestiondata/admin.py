from django.contrib import admin

from .models import Domain,Fr_Dom
from .models import (
    etablissement_client,
    etablissement_fournisseur,
    etablissement_client_simple,
    # Ajoute ici les autres modèles si besoin
)

# Register your models here.
admin.site.register(etablissement_client)

admin.site.register(Domain)

admin.site.register(Fr_Dom)

admin.site.register(etablissement_fournisseur)

admin.site.register(etablissement_client_simple)