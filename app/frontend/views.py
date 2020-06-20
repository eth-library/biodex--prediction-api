from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect


import requests

from backend.settings import BASE_URL
from taxonomy.models import Family, Subfamily, Genus, Species
from .forms import RequestTokenForm

def home_view(request):
    """View function for home page of site."""

    # # Generate counts of some of the main objects
    num_family = Family.objects.all().count()
    num_subfamily = Subfamily.objects.all().count()
    num_genus = Genus.objects.all().count()
    num_species = Species.objects.all().count()

    page_title = 'Home'
    
    context = {
        'page_title':page_title,
        'num_family': num_family,
        'num_subfamily': num_subfamily,
        'num_genus': num_genus,
        'num_species': num_species,

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'home.html', context=context)


def about_view(request):
    """View function for home page of site."""

    page_title = 'About'

    context = {
        'page_title':page_title}

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'about.html', context=context)


def login_view(request):
        
    page_title = 'Log In'

    loggedin = request.user.is_authenticated
    
    context= {
        'page_title':page_title,
        'login_message':'enter credentials to log in',
        'loggedin':request.user.is_authenticated,
        'loggedin_username': None,
    }

    if loggedin:
        loggedin_username = request.user.username
        context['loggedin_username'] = loggedin_username
        context['login_message'] = 'logged in as: {}'.format(loggedin_username)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            loggedin_username = request.user.username
            context['loggedin'] = request.user.is_authenticated
            context['loggedin_username'] = loggedin_username
            context['login_message'] = 'logged in as: {}'.format(loggedin_username)

        else:
            context['login_message'] = "Could not log in with provided credentials"

        return render(request, 'login.html', context=context)
    

    return render(request, 'login.html', context=context)


def logout_view(request):
        
    page_title = 'Log Out'

    loggedin = request.user.is_authenticated
    
    if loggedin:
        loggedin_username = request.user.username
    else:
        loggedin_username = None

    context= {
        'page_title':page_title,
        'login_message':'enter credentials to log in',
        'loggedin':request.user.is_authenticated,
        'loggedin_username': loggedin_username,
    }

    if request.method == 'POST':
        
        logout(request)

    return HttpResponseRedirect('/')


@login_required
def predict_view(request):
    """View function for home page of site."""

    page_title = 'Predict'
    prediction_results = {}
    authed = request.user.is_authenticated
    context = {
        'page_title':page_title,
        'prediction_results':prediction_results,
        'authed': authed
        }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'predict.html', context=context)
