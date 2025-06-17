from django.db import models

# Create your models here.


class etablissement_client(models.Model): # <----- this our client not fournisseur as u think 
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

class etablissement_fournisseur(models.Model): # <------- this fournisseur of our client  
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
    
class etablissement_client_simple(models.Model): # <------ this is our simple client who can buy in restaurent 
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

