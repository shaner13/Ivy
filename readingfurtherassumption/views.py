from django.shortcuts import render
from django.http import HttpResponseRedirect
import sys

# Create your views here.
def readingfurtherassumption(request):
    context = {'active': 'rfa'} # for navbar
    return render(request, 'readingfurtherassumption/rfa.html', context)