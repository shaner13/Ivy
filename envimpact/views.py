from django.shortcuts import render
from django.http import HttpResponseRedirect
import sys

# Create your views here.
def envimpact(request):
    if 'access_pages' in request.session:
        return render(request, 'envimpact/envimpact.html', request.session['env_context'])
    else:
        return HttpResponseRedirect('/')
        

