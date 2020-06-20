from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect

import requests

from backend.settings import BASE_URL
from taxonomy.models import Family, Subfamily, Genus, Species
from uploadforpredict_rest.views import predict_image_view
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

    if request.method == 'POST' and request.FILES["image"]:
        #use predeiction endpoint from the rest api
        prediction_request = predict_image_view(request)

        prediction_results = prediction_request.data['predictions']
        upload_img_name = prediction_request.data['uploaded_image_saved_name']
        upload_img_url = '/media/prediction_uploads/{}'.format(upload_img_name)
        prediction_results = prediction_request.data['predictions']
        context['prediction_results'] = prediction_results
        context['upload_img_url'] = upload_img_url
        
        return render(request,'predict.html', context=context)

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'predict.html', context=context)


def request_token_view(request):
        
    page_title = 'Log In'
    user_token = ''
    context= {
        'page_title':page_title,
        'user_token': user_token,        
    }

    if request.method == "POST":
        
        form = AuthenticationForm(data=request.POST)

        if True: #form.is_valid()
            
            username = form['username']
            password = form['password']

            data = {'username':username,
                    'password':password}

            token_url = 'http://' + BASE_URL + '/api/auth/token/login/'
            
            token_resp = requests.post(token_url, data)
            print(' token_resp', token_resp)
            if token_resp.status_code == 200:
                context['user_token'] = token_resp.json['Token']
        else:
            print('form not valid', request.POST)
        return render(request, 'request_token.html', context=context)

    form = AuthenticationForm()
    context['form'] = form

    return render(request, 'request_token.html', context=context)