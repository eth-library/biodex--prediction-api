from django.shortcuts import render

from taxonomy.models import Family, Subfamily, Genus, Species

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
