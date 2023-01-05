from django.urls import path
from . import views

urlpatterns = [
    path("",  views.PostListView.as_view(), name="index"),

    # paths dealing with user authentication
    path("signup", views.signup, name="sign_up"),
    path("signout", views.signout, name="sign_out"),
    path("signin", views.signin, name="sign_in"),

    # paths for dealing with creating/viewing posts
    path("newpost", views.newPost, name="create_post"),
    path("details/<int:pk>", views.PostDetailsView.as_view(), name="detail_view"),
]