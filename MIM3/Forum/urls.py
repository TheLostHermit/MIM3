from django.urls import path

# class based views can't use decorators for authentication
from django.contrib.auth.decorators import login_required, permission_required

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

    path("manage_posts", permission_required("Forum.can_post")(views.ManagePostsView.as_view()), name="manage_posts_view"),
    path("delete_post/<int:pk>", permission_required("Forum.can_post")(views.DeletePostView.as_view()), name="delete_post"),
    path("change_post/<int:pk>", permission_required("Forum.can_post")(views.ChangePostView.as_view()), name="change_post"),

    # paths for viewing people and organizations
    path("pinned", login_required(views.PinnedOrgsView.as_view()), name="pinned_view"),
    path("profile/<int:pk>", views.ProfileDetailView.as_view(), name="profile_view"),
    path("organization/<int:pk>", views.OrgDetailView.as_view(), name="organization_view"),

    # paths for pinning and unpinning organizations
    path("pinned/change_pin", views.ChangePinOrgView, name="change_pin"),

    # path for volunteering and managing volunteers for projects
    path("change_bids", views.ProjectBidView, name="change_bids"),
    path("your_projects", login_required(views.YourBidListView.as_view()), name="your_project_view"),
    path("delete_bid/<int:pk>", login_required(views.DeleteYourBidView.as_view()), name="delete_bid"),
    
]