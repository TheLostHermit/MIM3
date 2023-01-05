from django.shortcuts import render

# index page
def index(request):
    return render(request, "Forum/main_pages/index.html")
