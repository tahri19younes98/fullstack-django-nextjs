from rest_framework import serializers

from .models import etablissement_client, etablissement_fournisseur,etablissement_client_simple,Menu, Articles, TypeMenu, Url, Categorie

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


