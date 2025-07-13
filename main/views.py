from django.http import HttpResponseRedirect
from django.shortcuts import render

from main.models import Redirection

# Create your views here.
def site_redirection(request,id):
    try:
        red=Redirection.objects.get(id = id)
        return HttpResponseRedirect(red.site)
    except:
        return HttpResponseRedirect(f"http://127.0.0.1:8000/qrmainpage/restaurant/{id}/")
