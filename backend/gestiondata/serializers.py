from rest_framework import serializers

from .models import Famille, FamilleCharges, FamilleClients, FamilleFournisseur, FamilleProduction, LigneBonArtIn, LigneBonArtOut, LigneBonCmd, LigneBonEntreeStock, LigneBonLiv, LigneBonSortieStock, LigneBonTransfertIn, LigneBonTransfertOut, LigneDevis, MatierePremiere, RecetteProduction, Stock, StockMatierePremiere, etablissement_client, etablissement_fournisseur,etablissement_client_simple,Menu, Articles, TypeMenu, Url, Categorie, Charges, Devis

class etablissement_clientSerializer(serializers.ModelSerializer):
    class Meta:
        model = etablissement_client
        fields = '__all__'


class etablissement_fournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = etablissement_fournisseur
        fields = '__all__'

class etablissement_client_simpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = etablissement_client_simple
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = '__all__'

class TypeMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeMenu
        fields = '__all__'

class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = '__all__'


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

#-------------------------------new serializers--------------------------------
class FamilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Famille
        fields = '__all__'

class ChargesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charges
        fields = '__all__'


class DevisSerializer(serializers.Serializer):
    class Meta:
        model = Devis
        fields = '__all__'

class FamilleChargesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilleCharges
        fields = '__all__'

class FamilleFournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilleFournisseur
        fields = '__all__'

class FamilleClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilleClients
        fields = '__all__'


class FamilleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilleProduction
        fields = '__all__'

class MatierePremiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatierePremiere
        fields = '__all__'


class RecetteProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecetteProduction
        fields = '__all__'

class StockSerializer(serializers.Serializer):
    class Meta:
        model = Stock
        fields = '__all__'

class StockMatierePremiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMatierePremiere
        fields = '__all__'

#--------------------------------------LigneBon --------------------------------------

class LigneBonArtInSerializer(serializers.Serializer):
    class Meta:
        model = LigneBonArtIn
        fields = '__all__'

class LigneBonArtOutSerializer(serializers.Serializer):
    class Meta:
        model = LigneBonArtOut
        fields = '__all__'

class LigneBonCmdSerializer(serializers.Serializer):
    class Meta:
        model = LigneBonCmd
        fields = '__all__'

class LigneBonEntreeStockSerializer(serializers.Serializer):
    class Meta:
        model = LigneBonEntreeStock
        fields = '__all__'

class LigneBonLivSerializer(serializers.Serializer):
    class Meta:
        model = LigneBonLiv
        fields = '__all__'

class LigneBonSortieStockSerializer(serializers.Serializer):
    class Meta:
        model = LigneBonSortieStock
        fields = '__all__'

class LigneBonTransfertInSerializer(serializers.Serializer):
    class Meta:
        model = LigneBonTransfertIn
        fields = '__all__'

class LigneBonTransfertOutSerializer(serializers.Serializer):
    class Meta:
        model = LigneBonTransfertOut
        fields = '__all__'


class LigneDevisSerializer(serializers.Serializer):
    class Meta:
        model = LigneDevis
        fields = '__all__'



#--------------------------------------Bon --------------------------------------
from .models import BonArtIn, BonArtOut, BonCmd, BonEntreeStock, BonLiv, BonSortieStock, BonTransfertIn, BonTransfertOut

class BonArtInSerializer(serializers.Serializer):
    class Meta:
        model = BonArtIn
        fields = '__all__'

class BonArtOutSerializer(serializers.Serializer):
    class Meta:
        model = BonArtOut
        fields = '__all__'

class BonCmdSerializer(serializers.Serializer):
    class Meta:
        model = BonCmd
        fields = '__all__'

class BonEntreeStockSerializer(serializers.Serializer):
    class Meta:
        model = BonEntreeStock
        fields = '__all__'

class BonLivSerializer(serializers.Serializer):
    class Meta:
        model = BonLiv
        fields = '__all__'

class BonSortieStockSerializer(serializers.Serializer):
    class Meta:
        model = BonSortieStock
        fields = '__all__'


class BonTransfertInSerializer(serializers.Serializer):
    class Meta:
        model = BonTransfertIn
        fields = '__all__'

class BonTransfertOutSerializer(serializers.Serializer):
    class Meta:
        model = BonTransfertOut
        fields = '__all__'