# imports for rendering/constructing views
from django.shortcuts import render

# imports for authentication
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

# imports for navigating around the site
from django.http import HttpResponseRedirect
from django.urls import reverse

# importing models and forms from other files in this folder
from .forms import *
from .models import *

# index page
def index(request):
    return render(request, "Forum/main_pages/index.html")

# sign up, sign in and sign out functions
def signup(request):

    HTML_PAGE = "Forum/auth_pages/signup.html"

    # if the form is being submitted
    if request.method == "POST":

        create_profile_form = NewProfileForm(request.POST)

        if create_profile_form.is_valid():

            try:
                user = create_profile_form.save()

            except IntegrityError:
                return render(request, HTML_PAGE, {
                "form": create_profile_form,
                "message": "integrity error"
                })

            login(request, user)
            return (HttpResponseRedirect(reverse('index')))

        else:
            return render(request, HTML_PAGE, {
                "form": create_profile_form,
            })

    #if the form is not being submitted
    return render(request, HTML_PAGE, {
        "form": NewProfileForm()
    })

def signout(request):
    logout(request)
    return (HttpResponseRedirect(reverse('index')))

def signin(request):

    HTML_PAGE = "Forum/auth_pages/signin.html"

    # if the form on the page is being submitted    
    if request.method == "POST":

        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]

        # if the user did not use their username
        if not username.strip():

            # get their profile and use their username for them
            profile_obj = Profile.objects.get(first_name=first_name, last_name = last_name)
            username = profile_obj.username

        profile = authenticate(request, username=username, password=password)
        
        if profile:
            login(request, profile)
            return HttpResponseRedirect(reverse("index"))

        else:

            # error message
            return render(request, HTML_PAGE, {
                "message": "invalid credentials"
            })

    else:
        return render(request, HTML_PAGE) 