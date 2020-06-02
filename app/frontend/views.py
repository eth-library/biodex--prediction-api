from django.shortcuts import render

from taxonomy.models import Family

def home_view(request):
    """View function for home page of site."""

    # # Generate counts of some of the main objects
    num_families = Family.objects.all().count()
    # num_instances = BookInstance.objects.all().count()
    
    # # Available books (status = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # # The 'all()' is implied by default.    
    # num_authors = Author.objects.count()
    
    context = {
        'num_families': num_families,
        # 'num_instances': num_instances,
        # 'num_instances_available': num_instances_available,
        # 'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'home.html', context=context)


def about_view(request):
    """View function for home page of site."""


    # Render the HTML template index.html with the data in the context variable
    return render(request, 'about.html', context=None)