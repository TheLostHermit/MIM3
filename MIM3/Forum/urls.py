from django.urls import path
from . import views

urlpatterns = [
    path("",  views.index, name="index"),

    # paths dealing with user authentication
    path("signup", views.signup, name="sign_up"),
    path("signout", views.signout, name="sign_out"),
    path("signin", views.signin, name="sign_in"),
]