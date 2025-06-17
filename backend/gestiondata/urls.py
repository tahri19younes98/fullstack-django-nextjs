from django.urls import path
from . import views

app_name = "gestiondata"
 
urlpatterns = [  
 # Pages
    path("clientpage", views.Clientpage, name="client_page"),
    path("menu", views.menu_page, name="menu_page"),
    path("articles", views.articles_page, name="articles_page"), 
    path("url", views.url_page, name="url_page"),
    path("typemenu", views.typemenu_page, name="typemenu_page"),  
    path("categorie/", views.categorie_page, name="categorie_page"),
    path("FournisseurFournisseur", views.fournisseur_fournisseur_page, name="fournisseur_fournisseur_page"),
    path("FournisseurClient", views.fournisseur_client_page, name="fournisseur_client_page"),

    # List view (HTML)
    path('clients/', views.liste_clients, name='liste_clients'),

    # REST API ENDPOINTS for Etablissement_client
    path("api/etablissementClient/", views.etablissement_clientListCreateView.as_view(), name="fournisseur_list"),
    path("api/etablissementClient/<int:pk>/", views.etablissement_clientDetailView.as_view(), name="fournisseur_detail"),
    # REST API ENDPOINTS for Fournisseur_fournisseur
    path("api/etablissement_fournisseur/", views.etablissement_fournisseurListCreateView.as_view(), name="fournisseur_fournisseur_list"),
    path("api/etablissement_fournisseur/<int:pk>/", views.etablissement_fournisseurDetailView.as_view(), name="fournisseur_fournisseur_detail"),
    # REST API ENDPOINTS for Fournisseur_client
    path("api/etablissement_client_simple/", views.etablissement_client_simpleListCreateView.as_view(), name="fournisseur_client_list"),
    path("api/etablissement_client_simple/<int:pk>/", views.etablissement_client_simpleDetailView.as_view(), name="fournisseur_client_detail"),
    # REST API ENDPOINTS for Menu
    path("api/menus/", views.MenuListCreateView.as_view(), name="menu_list"),
    path("api/menus/<int:pk>/", views.MenuDetailView.as_view(), name="menu_detail"),
    # REST API ENDPOINTS for Article
    path("api/articles/", views.ArticlesListCreateView.as_view(), name="article_list"),
    path("api/articles/<int:pk>/", views.ArticlesDetailView.as_view(), name="article_detail"),

    # REST API ENDPOINTS for URL
    path("api/urls/", views.UrlListCreateView.as_view(), name="url_list"),
    path("api/urls/<int:pk>/", views.UrlDetailView.as_view(), name="url_detail"),
  # Other CRUD endpoints
   # path("create_menu/", views.create_menu),
   # path("update_menu/<int:menu_id>/", views.update_menu),
   # path("delete_menu/<int:menu_id>/", views.delete_menu),
   
   #path("create_article/", views.create_article),
   # path("update_article/<int:article_id>/", views.update_article),
   # path("delete_article/<int:article_id>/", views.delete_article),
   
   # path("create_url/", views.create_url),
    path("create_typemenu/", views.create_typemenu),
    path("create_categorie/", views.create_categorie),



    # Selective button endpoints
    path("api/typemenus_urls/", views.get_typemenus_and_urls),
    path("api/categories/", views.get_categories),


]




