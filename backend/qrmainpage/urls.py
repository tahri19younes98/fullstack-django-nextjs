from django.urls import path

from . import views

app_name = "qrmainpage"
urlpatterns = [
    path("",views.index,name="index"),
    #path('download-menu-pdf/', views.download_menu_pdf, name='download_menu_pdf'),
    path('download_pdf/', views.download_pdf, name='download_pdf'),
    path('restaurant/', views.restaurant_qr_view, name='restaurant_qr'),
    
]
