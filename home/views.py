from django.shortcuts import render
from django.http import HttpResponse
import sys

# Create your views here.
def home(request):
    context = {'active': 'home'} # for navbar
    return render(request, 'home/home.html', context)