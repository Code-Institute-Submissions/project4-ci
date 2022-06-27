from django.shortcuts import render


def index(request):
    """
    Function render home page
    Extra context to be used by template
    """
    page_title = "Home"
    return render(request, 'index.html', {'page_title': page_title})
