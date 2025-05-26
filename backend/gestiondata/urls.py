from django.urls import path
from . import views

app_name = "gestiondata"

urlpatterns = [
 # Pages
    path("fournisseur", views.Fournisseurpage, name="fournisseur"),
    path("menu", views.menu_page, name="menu_page"),
    path("articles", views.articles_page, name="articles_page"), 
    path("url", views.url_page, name="url_page"),
    path("typemenu", views.typemenu_page, name="typemenu_page"),  
    path("categorie/", views.categorie_page, name="categorie_page"),

    # List view (HTML)
    path('fournisseurs/', views.liste_fournisseurs, name='liste_fournisseurs'),

    # REST API ENDPOINTS for Fournisseur
    path("api/fournisseurs/", views.FournisseurListCreateView.as_view(), name="fournisseur_list"),
    path("api/fournisseurs/<int:pk>/", views.FournisseurDetailView.as_view(), name="fournisseur_detail"),
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




