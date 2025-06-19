from django.db import models

# Create your models here.


class etablissement_client(models.Model):
    name = models.CharField(max_length=100)
    localisation = models.CharField(max_length=100)
    address = models.TextField()
    type = models.IntegerField()
    domaine = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    art = models.CharField(max_length=100)
    nis = models.CharField(max_length=20)
    nif = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class etablissement_fournisseur(models.Model): 
    name = models.CharField(max_length=100)
    localisation = models.CharField(max_length=100)
    address = models.TextField()
    type = models.IntegerField()
    domaine = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    art = models.CharField(max_length=100)
    nis = models.CharField(max_length=20)
    nif = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class etablissement_client_simple(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
     

    def __str__(self):
        return self.name


class List_Client_ClientSimple(models.Model):
    id_client_simple = models.ManyToManyField(etablissement_client_simple)
    id_client = models.ManyToManyField(etablissement_client)


class Domain(models.Model):
    name = models.CharField(max_length=100)
    fournisseur = models.ForeignKey(etablissement_client, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (Fournisseur: {self.fournisseur.name})"


class Fr_Dom(models.Model):
      id_f = models.ForeignKey(etablissement_client, on_delete=models.CASCADE)
      id_d = models.ForeignKey(Domain,  on_delete=models.CASCADE)
      nom_domain = models.CharField(max_length=100,default='Unknown') # <--------- i add new attribute 
      def __str__(self): 
          return  f"{self.id_f} - {self.id_d}"


class TypeFr(models.Model):
    name = models.CharField(max_length=100)
    id_fournisseur = models.ForeignKey(etablissement_client, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Url(models.Model):
     name_url =  models.CharField(max_length=100)
     four_url = models.ForeignKey(etablissement_client, on_delete=models.CASCADE, related_name='urls')
     

     def __str__(self):
         return self.name_url
     

class Menu(models.Model):
    list_Menu = models.CharField(max_length=100)
   # list_Price = models.FloatField()
    extension = models.CharField(max_length=100,null=True,blank=True)
    articles = models.ManyToManyField('Articles', through='Menu_Article')
    type_menu = models.ForeignKey('TypeMenu', on_delete=models.CASCADE)
    Url = models.ForeignKey('Url', on_delete=models.CASCADE, related_name='menus')
    def __str__(self):
        return self.list_Menu ,self.list_Price


class Articles(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    code_barre = models.BigIntegerField()
    Categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE,related_name='articles')
    qte = models.IntegerField(default=0)
    image = models.CharField(max_length=500, blank=True, null=True)
    def __str__(self):
        return self.name,self.price,self.code_barre


    


class Menu_Article(models.Model):
    id_Menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    id_Articles = models.ForeignKey(Articles, on_delete=models.CASCADE)
    Price = models.FloatField()

    def __str__(self):
        return self.Price


#here i wanna rebuild
class TypeMenu(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Categorie(models.Model):
    name_cat = models.CharField(max_length=100)

    def __str__(self):
        return self.name_cat


class Famille(models.Model):
    name_fam = models.CharField(max_length=100)
    id_cat = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='familles')
    def __str__(self):
        return self.name_fam

class Sfamille(models.Model):
    
    famille = models.ForeignKey(Famille, on_delete=models.CASCADE)
    name_sfam = models.CharField(max_length=100)
    def __str__(self):
        return self.id_fm


#----------------------------------new models----------------------------------#

class code_barre(models.Model):
    code = models.BigIntegerField(unique=True)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='codes_barre')
   # user = models.IntegerField(default=0)  # Assuming this is for tracking the user who created the code 
    def __str__(self):
        return str(self.code)
    

class Charges(models.Model): 
    designation = models.CharField(max_length=50, blank=True, null=True)
    montant = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    date = models.DateTimeField(blank=True, null=True)
    periode = models.DecimalField(max_digits=19, decimal_places=0, blank=True, null=True)
   # user = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.designation} - {self.montant} - {self.date}"
    


class Devis(models.Model):
    date = models.DateTimeField()
    propreot = models.IntegerField(default=0)
    montant = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    numeros = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.propreot} - {self.montant} - {self.numeros}"
    

class FamilleCharges(models.Model):
   # idFamille = models.ForeignKey(Famille, on_delete=models.CASCADE, related_name='famille_charges')
    nom = models.CharField(max_length=100)
    codif = models.CharField(max_length=100)
    image = models.CharField(max_length=500, blank=True, null=True)
    #user = models.IntegerField(default=0)    
    def __str__(self):
        return self.nom
    
class FamilleFournisseur(models.Model):
    # idFamille = models.ForeignKey(Famille, on_delete=models.CASCADE, related_name='famille_fournisseur')
    nom = models.CharField(max_length=100)
    codif = models.CharField(max_length=100)
    image = models.CharField(max_length=500, blank=True, null=True)
    #user = models.IntegerField(default=0)

    def __str__(self):
        return self.nom
    

class FamilleClients(models.Model):
    # idFamille = models.ForeignKey(Famille, on_delete=models.CASCADE, related_name='famille_clients')
    nom = models.CharField(max_length=100)
    codif = models.CharField(max_length=100)
    image = models.CharField(max_length=500, blank=True, null=True)
    #user = models.IntegerField(default=0)

    def __str__(self):
        return self.nom
    
class FamilleProduction(models.Model):
    # idFamille = models.ForeignKey(Famille, on_delete=models.CASCADE, related_name='famille_production')
    nom = models.CharField(max_length=100)
    codif = models.CharField(max_length=100)
    image = models.CharField(max_length=500, blank=True, null=True)
    #user = models.IntegerField(default=0)

    def __str__(self):
        return self.nom
    

#------------------------------------separate models----------------------------------#

class LigneBonArtIn(models.Model):
   # id_bon = models.IntegerField(default=0)
    art = models.IntegerField(default=0)
    qte = models.IntegerField(default=0)
    prix = models.DecimalField(max_digits=24, decimal_places=6, default=0)
   # user = models.IntegerField(default=0)
    nbrcolis = models.IntegerField(default=0)

class LigneBonArtOut(models.Model):
  #  id_bon = models.IntegerField(default=0)
    art = models.IntegerField(default=0)
    qte = models.IntegerField(default=0)
    prix = models.DecimalField(max_digits=24, decimal_places=6, default=0)
  #  user = models.IntegerField(default=0)
    nbrcolis = models.IntegerField(default=0)
    prix_achat = models.DecimalField(max_digits=24, decimal_places=6, default=0)

class LigneBonCmd(models.Model):
  #  id_bon = models.IntegerField(default=0)
    art = models.IntegerField(default=0)
    qte = models.IntegerField(default=0)
    prix = models.DecimalField(max_digits=24, decimal_places=6, default=0)
  #  user = models.IntegerField(default=0)
    nbrcolis = models.IntegerField(default=0)

class LigneBonEntreeStock(models.Model):
  #  id_bon = models.IntegerField(default=0)
    art = models.IntegerField(default=0)
    qte = models.IntegerField(default=0)
    prix = models.DecimalField(max_digits=24, decimal_places=6, default=0)
  #  user = models.IntegerField(default=0)
    nbrcolis = models.IntegerField(default=0)

class LigneBonLiv(models.Model):
  #  id_bon = models.IntegerField(default=0)
    art = models.IntegerField(default=0)
    qte = models.IntegerField(default=0)
    prix = models.DecimalField(max_digits=24, decimal_places=6, default=0)
  # user = models.IntegerField(default=0)
    nbrcolis = models.IntegerField(default=0)

class LigneBonSortieStock(models.Model):
  #  id_bon = models.IntegerField(default=0)
    art = models.IntegerField(default=0)
    qte = models.IntegerField(default=0)
    prix = models.DecimalField(max_digits=24, decimal_places=6, default=0)
  #  user = models.IntegerField(default=0)
    nbrcolis = models.IntegerField(default=0)

class LigneBonTransfertIn(models.Model):
  #  id_bon = models.IntegerField(default=0)
    art = models.IntegerField(default=0)
    qte = models.IntegerField(default=0)
    prix = models.DecimalField(max_digits=24, decimal_places=6, default=0)
  #  user = models.IntegerField(default=0)

class LigneBonTransfertOut(models.Model):
  #  id_bon = models.IntegerField(default=0)
    art = models.IntegerField(default=0)
    qte = models.IntegerField(default=0)
    prix = models.DecimalField(max_digits=24, decimal_places=6, default=0)
  #  user = models.IntegerField(default=0)

class LigneDevis(models.Model):
  #  id_bon = models.IntegerField(default=0)
    art = models.IntegerField(default=0)
    qte = models.IntegerField(default=0)
    prix = models.DecimalField(max_digits=24, decimal_places=6, default=0)
  # user = models.IntegerField(default=0)
    nbrcolis = models.IntegerField(default=0)

class MatierePremiere(models.Model):
    article = models.CharField(max_length=50)
    code_barre = models.CharField(max_length=13)
    famille = models.IntegerField(default=0)
    image = models.CharField(max_length=500, blank=True, null=True)
    TVA = models.IntegerField(default=0)
    user = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=24, decimal_places=6, default=0)
   # Prix_achat_last = models.DecimalField(max_digits=24, decimal_places=6, default=0)
   # prix_vente = models.DecimalField(max_digits=24, decimal_places=6, default=0)
   # prix_min = models.DecimalField(max_digits=24, decimal_places=6, default=0)
   # PMP_encours = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    qte = models.IntegerField(default=0)

    def __str__(self):
        return self.article
    
class RecetteProduction(models.Model):
    idart = models.ForeignKey(Articles, on_delete=models.CASCADE)
    idmatierepremier = models.ForeignKey(MatierePremiere, on_delete=models.CASCADE)
    qte = models.IntegerField(default=0)
    prix_revient = models.DecimalField(max_digits=24, decimal_places=6, default=0)
    qteresultat = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.idart} - {self.idmatierepremier} - {self.qte} - {self.prix_revient} - {self.qteresultat}"
    

class Stock(models.Model):
    qte = models.IntegerField(default=0)
    idart = models.ForeignKey(Articles, on_delete=models.CASCADE)
   # user = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.idart} - {self.qte}"
    

class StockMatierePremiere(models.Model):
    qte = models.IntegerField(default=0)
    idart = models.ForeignKey(MatierePremiere, on_delete=models.CASCADE)
   # user = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.idart} - {self.qte}"
    

