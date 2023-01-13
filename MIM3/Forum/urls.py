from django.urls import path

# class based views can't use decorators for authentication
from django.contrib.auth.decorators import login_required, permission_required

# importing all the view functions/classes for the urls to use
from . import views

urlpatterns = [

    # general pages
    path("",  views.PostListView.as_view(), name="index"),
    path("error", views.ErrorView, name="error_view"),
    path("permission_denied", views.PermissionDeniedView, name="permission_denied"),

    # paths dealing with user authentication and editing
    path("signup", views.signup, name="sign_up"),
    path("signout", views.signout, name="sign_out"),
    path("login", views.signin, name="login"),
    path("edit_profile", views.ChangeProfileView, name="edit_profile"),

    # paths for dealing with creating/viewing posts
    path("newpost", views.newPost, name="create_post"),
    path("details/<int:pk>", views.PostDetailsView.as_view(), name="detail_view"),
    path("postsby/<int:org_pk>", views.PostsByOrgView.as_view(), name="posts_by_org"),

    path("manage_posts", permission_required("Forum.can_post")(views.ManagePostsView.as_view()), name="manage_posts_view"),
    path("delete_post/<int:pk>", permission_required("Forum.can_post")(views.DeletePostView.as_view()), name="delete_post"),
    path("change_post/<int:pk>", permission_required("Forum.can_post")(views.ChangePostView.as_view()), name="change_post"),
    path("manage_imgs/<int:post_pk>", permission_required("Forum.can_post")(views.ManagePostImgsView.as_view()), name="manage_imgs"),
    path("change_imgs/<int:post_pk>", views.ChangeImgView, name="change_imgs"),
    path("manage_events/<int:post_pk>", permission_required("Forum.can_post")(views.ManageEventsView.as_view()), name="manage_events"),
    path("change_event/", views.ChangeEventView, name="change_event"),

    # paths for viewing people and organizations
    path("pinned", login_required(views.PinnedOrgsView.as_view()), name="pinned_view"),
    path("profile/<int:pk>", views.ProfileDetailView.as_view(), name="profile_view"),
    path("organization/<int:pk>", views.OrgDetailView.as_view(), name="organization_view"),
    path("manage_volunteers/<str:action>", views.ManageVolunteersView, name="manage_volunteers"),
    path("view_volunteers/<int:event_pk>/<str:status>", permission_required("Forum.can_post")(views.VolunteerListView.as_view()), name="view_volunteers"),

    # paths for pinning and unpinning organizations
    path("pinned/change_pin", views.ChangePinOrgView, name="change_pin"),

    # path for volunteering and managing volunteers for projects
    path("change_bids", views.ProjectBidView, name="change_bids"),
    path("your_projects", login_required(views.YourBidListView.as_view()), name="your_project_view"),
    path("delete_bid/<int:pk>", login_required(views.DeleteYourBidView.as_view()), name="delete_bid"),
    path("change_status", views.ChangeVolunteerView, name="change_status"),

    # paths for sending/seeing messages
    path("send_message/<int:event_pk>/<str:status>", permission_required("Forum.can_post")(views.NewMessageView.as_view()), name = "send_message"),
    path("sent_messages", permission_required("Forum.can_post")(views.SentMessagesView.as_view()), name = "sent_messages"),
    path("received_messages", login_required(views.ReceivedMessagesView.as_view()), name = "received_messages"),
    path("delete_message/<int:pk>", permission_required("Forum.can_post")(views.DeleteMessagesView.as_view()), name = "delete_message"),

]