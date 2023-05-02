import requests
from backend.settings import BASE_URL, EMAIL_CONTACT_LIST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from taxonomy.models import Family, Genus, Species, Subfamily
from uploadforpredict.views import predict_image_view


def home_view(request):
    """View function for home page of site."""

    # # Generate counts of some of the main objects
    num_family = Family.objects.all().count()
    num_subfamily = Subfamily.objects.all().count()
    num_genus = Genus.objects.all().count()
    num_species = Species.objects.all().count()

    page_title = 'Home'

    context = {
        'page_title': page_title,
        'num_family': num_family,
        'num_subfamily': num_subfamily,
        'num_genus': num_genus,
        'num_species': num_species,

    }

    # Render the HTML template home.html with the data in the context variable
    return render(request, 'home.html', context=context)


def about_view(request):
    """View function for about page of site."""

    page_title = 'About'

    context = {
        'page_title': page_title
    }

    return render(request, 'about.html', context=context)


def legal_view(request):
    """View function for privacy policy page of site."""

    page_title = 'Legal Notice'

    context = {
        'page_title': page_title
    }

    return render(request, 'legal_notice.html', context=context)


def contact_view(request):
    """View function for contact page."""

    page_title = 'Contact'

    context = {
        'page_title': page_title
    }

    if request.method == 'POST':

        contact_name = request.POST['contact_name']
        contact_email = request.POST['contact_email']
        contact_subject = request.POST['contact_subject']
        contact_message = request.POST['contact_message']

        forward_message = """
from: {contact_name}  
email: {contact_email}  
subject: {contact_subject}  
message:   
{contact_message}
""".format(contact_name=contact_name,
            contact_email=contact_email,
            contact_subject=contact_subject,
            contact_message=contact_message)

        # send the contact email
        send_mail('BIODEX_CONTACT: {}'.format(contact_subject),
                  forward_message,
                  contact_email,
                  EMAIL_CONTACT_LIST,
                  )

        context['response_message'] = "Thanks for contacting us {}, we look forward to reading your message".format(
            contact_name)

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'contact.html', context=context)


def login_view(request):

    page_title = 'Log In'

    loggedin = request.user.is_authenticated

    context = {
        'page_title': page_title,
        'login_message': 'enter credentials to log in',
        'loggedin': request.user.is_authenticated,
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
            context['login_message'] = 'logged in as: {}'.format(
                loggedin_username)

            return HttpResponseRedirect('/predict/')

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

    context = {
        'page_title': page_title,
        'login_message': 'enter credentials to log in',
        'loggedin': request.user.is_authenticated,
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
        'page_title': page_title,
        'prediction_results': prediction_results,
        'authed': authed
    }

    if request.method == 'POST' and request.FILES["image"]:
        # use prediction endpoint from the rest api
        prediction_request = predict_image_view(request)
        prediction_results = prediction_request.data['predictions']
        print('top prediction: \n', prediction_results[0], '\n')
        upload_img_name = prediction_request.data['uploaded_image_saved_name']
        upload_img_url = '/media/image/prediction_uploads/{}'.format(
            upload_img_name)
        context['prediction_results'] = prediction_results
        context['upload_img_url'] = upload_img_url

        return render(request, 'predict.html', context=context)

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'predict.html', context=context)
