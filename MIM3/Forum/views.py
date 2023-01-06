# imports for rendering/constructing views
from django.shortcuts import render
from django.views.generic import ListView, DetailView

# imports for authentication
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.db import IntegrityError

# imports for navigating around the site
from django.http import HttpResponseRedirect
from django.urls import reverse

# importing models and forms from other files in this folder
from .forms import * # models are imported through this as well

# index page
def index(request):
    return render(request, "Forum/main_pages/index.html")

# in the case of permission required the user is actually redirected to the index
# (Consider adding "access denied" message of some sort to this route instead)
@login_required(login_url= 'sign_in')
@permission_required('Forum.can_post', login_url= 'index')
def newPost(request):
    HTML_PAGE = "Forum/post_pages/create_post.html"

    image_formset = ImageFormset(prefix='image', queryset=PostImage.objects.none())
    event_formset = EventFormset(prefix='event', queryset=Event.objects.none())

    if request.method == "GET":

        return render(request, HTML_PAGE, {
            'image_formset': image_formset,
            'post_form' : NewPostForm(),
            'event_formset' : event_formset
        })

    # if the form is being submitted
    elif request.method == "POST":

        post_form = NewPostForm(request.POST)

        # validate and save the post
        if post_form.is_valid():
            
            new_post = post_form.save(commit=False)

            # find the person who created this post in order to add their organization to it
            post_author = Profile.objects.get(pk=request.user.pk)
            new_post.author = post_author
            if post_author.membership: new_post.organization = post_author.membership

            new_post.save()

            # create and save the images if the post is valid overall
            image_form = ImageFormset(request.POST, request.FILES, prefix="image")

            if image_form.is_valid():

                for form in image_form:

                    image = form.save(commit=False)

                    default_image = PostImage._meta.get_field('image').get_default()

                    if (image.image != default_image):
                        image.post = new_post

                        print("this is not the default image")
                        image.save()
            
            # create and save events for the project if it is a project
            if new_post.is_project:

                event_form = EventFormset(request.POST, prefix='event')

                if event_form.is_valid():

                    for form in event_form:

                        event = form.save(commit=False)
                        event.post = new_post

                        if event.date < timezone.now().date():event.open = False
                        
                        event.save()
            
            return (HttpResponseRedirect(reverse('index')))

        else:

            # if the post is not valid return the information to be edited
            return render(request, HTML_PAGE, {
            'image_formset': image_form,
            'post_form' : post_form,
            'event_formset' : event_form
        })

# view used for the feed which renders a list of all the posts made to the forum
class PostListView(ListView):

    # brings up the template because this class has a default template route
    template_name = "Forum/main_pages/index.html"

    # the model that is to be listed
    model = Post
    context_object_name = 'post_list'

    # allowing pagination (putting the objects into multiple pages)
    # *note: 2 is a placeholder until more data is used to populate the database
    paginate_by = 2

    # modifying the queryset to display in reverse chronological order
    def get_queryset(self, *args, **kwargs):
        queryset = super(PostListView, self).get_queryset(*args, **kwargs)
        queryset = queryset.order_by("-timestamp")
        return queryset

 # view used for the feed which renders a the details of a chosen post 
class PostDetailsView(DetailView):

    model = Post

    # overriding default template path
    template_name = "Forum/post_pages/view_post.html"

class PinnedOrgsView(ListView):

    model = Organization

    # overriding default template path
    template_name = "Forum/main_pages/pinned.html"

    def get_queryset(self, *args, **kwargs):

        queryset = super(PinnedOrgsView, self).get_queryset(*args, **kwargs)
        return queryset.filter(followers=self.request.user.pk)
        
# detail views for organizations and people
# view used for displaying a profile's information
class ProfileDetailView(DetailView):

    model = Profile

    # overriding default template path
    template_name = "Forum/detail_pages/profile_details.html"

# detail views for organizations and people
# view used for displaying an organization's information
class OrgDetailView(DetailView):

    model = Organization

    # overriding default template path
    template_name = "Forum/detail_pages/org_details.html"

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