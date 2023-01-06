from django.urls import path

# class based views can't use decorators for authentication
from django.contrib.auth.decorators import login_required

# importing all the view functions/classes for the urls to use
from . import views

urlpatterns = [
    path("",  views.PostListView.as_view(), name="index"),

    # paths dealing with user authentication
    path("signup", views.signup, name="sign_up"),
    path("signout", views.signout, name="sign_out"),
    path("login", views.signin, name="login"),

    # paths for dealing with creating/viewing posts
    path("newpost", views.newPost, name="create_post"),
    path("details/<int:pk>", views.PostDetailsView.as_view(), name="detail_view"),
    path("postsby/<int:org_pk>", views.PostsByOrgView.as_view(), name="posts_by_org"),

    # paths for viewing people and organizations
    path("pinned", login_required(views.PinnedOrgsView.as_view()), name="pinned_view"),
    path("profile/<int:pk>", views.ProfileDetailView.as_view(), name="profile_view"),
    path("organization/<int:pk>", views.OrgDetailView.as_view(), name="organization_view"),

    # paths for pinning and unpinning organizations
    path("pinned/unpin", views.UnpinOrgView, name="unpinning_view"),
]