from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.site_redirection, name='site_redirection'),
]