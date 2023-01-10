# imports for rendering/constructing views
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, UpdateView

# imports for authentication
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.db import IntegrityError

# imports for navigating around the site
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

# imports for processing requests from javascript
from django.http.response import JsonResponse
import json

# importing models and forms from other files in this folder
from .forms import * # models are imported through this as well

# the number of list items to display before pagination is controlled by this global variable
PAGINATE_NO = 2

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
    paginate_by = PAGINATE_NO

    # modifying the queryset to display in reverse chronological order
    def get_queryset(self, *args, **kwargs):
        queryset = super(PostListView, self).get_queryset(*args, **kwargs)
        queryset = queryset.order_by("-timestamp")

        # looks through all the dates and updates their status
        for post_entry in queryset:

            if post_entry.is_project:
                project_events = Event.objects.filter(post = post_entry)
                
                for event in project_events:

                    # if an event has passed close it and mark all bids as passed
                    if event.date < timezone.now().date():

                        event_bids = event.bids.all()

                        for bid in event_bids:

                            bid.status = "CP"
                            bid.save()

                        event.open = False
                        event.save()

        return queryset

 # view used for the feed which renders a the details of a chosen post 
class PostDetailsView(DetailView):

    model = Post
    context_object_name = 'post'

    # overriding default template path
    template_name = "Forum/post_pages/view_post.html"

    # checking the volunteer objects to see if the user has volunteered for this project
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs.get('pk'))

        if post.is_project:

            # this query returns all events for this post that the user has volunteered for.
            # the returned queryset is checked against when it is checked whether a user has already
            # volunteered for a time slot
            post_events = Event.objects.filter(post=post, bids__bidder__pk=self.request.user.pk)               
            context['post_events'] = post_events

        return context


# view rendering a list of all the organizations the user has pinned
class PinnedOrgsView(ListView):

    model = Organization

    # overriding default template path
    template_name = "Forum/main_pages/pinned.html"

    def get_queryset(self, *args, **kwargs):

        queryset = super(PinnedOrgsView, self).get_queryset(*args, **kwargs)
        return queryset.filter(followers=self.request.user.pk)

# view rendering the list of posts only made my a specific organization
class PostsByOrgView(ListView):

    model = Post

    paginate_by = PAGINATE_NO

    # overriding default template path
    template_name = "Forum/main_pages/index.html"

    def get_queryset(self, *args, **kwargs):

        # gets posts by a particular organization
        queryset = super(PostsByOrgView, self).get_queryset(*args, **kwargs)
        queryset = queryset.filter(organization = self.kwargs['org_pk'])
        return queryset.order_by("-timestamp")   

# view for seeing all the projects you volunteered for
class YourBidListView(ListView):

    model = Bid
    # overriding default template path
    template_name = "Forum/dash_pages/user_bids.html"

    def get_queryset(self, *args, **kwargs):

        queryset = super(YourBidListView, self).get_queryset(*args, **kwargs)
        return queryset.filter(bidder=self.request.user.pk).order_by("event__date")

# deletes bid from the bid list 
class DeleteYourBidView(DeleteView):

    model = Bid

    # overriding default template path
    template_name = "Forum/util_pages/delete_bid.html"

    def get_success_url(self):
        return reverse('your_project_view')

# dashboard view gets all the projects/posts of an organization
class ManagePostsView(ListView):

    model = Post

    # overriding the default template path
    template_name = "Forum/dash_pages/org_posts.html"

    def get_queryset(self, *args, **kwargs):

        queryset = super(ManagePostsView, self).get_queryset(*args, **kwargs)

        # return the queryset filtered by the user's organization all in reverse chronological order
        
        current_profile = Profile.objects.get(pk=self.request.user.pk)
        return queryset.filter(organization=current_profile.membership).order_by("-timestamp")


# view deletes a selected post object and redirects to the organization dashboard
class DeletePostView(DeleteView):

    model = Post

    # overriding the default template path
    template_name = "Forum/util_pages/delete_post.html"

    def get_success_url(self):
        return reverse('manage_posts_view')

# view changes the title or body of a selected post
class ChangePostView(UpdateView):

    model = Post
    fields = ['title', 'body']

    # overriding the default template path
    template_name = "Forum/post_pages/change_post.html"

    # when done redirect to the post which was changed
    def get_success_url(self):
        return reverse('detail_view', kwargs={'pk':self.object.id})



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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_pinned = self.object.followers.filter(pk=self.request.user.pk)
        context['pinned'] = is_pinned.exists()

        return context

# view which is called when the user unpins and organization
def ChangePinOrgView(request):

    if request.method == "PUT":

        data = json.loads(request.body)

        if data.get('org_pk') is not None and data.get('action') is not None:

            target_org_pk = data['org_pk']
            unpinning = data['action'] == 'unpin' and True or False
            profile = Profile.objects.get(pk=request.user.pk)

            if unpinning:

                # see if the user's profile has the organization that needs to be unpinned
                for organization in profile.pinned.all():

                    if int(organization.pk) == int(target_org_pk):

                        profile.pinned.remove(organization)
                        profile.save()
                        return HttpResponse(status=204)

                # if the entire for loop has gone and no organization has been found return an error
                return JsonResponse({
                    "error":"organization did not match any the user has pinned"
                }, status=400)

            else:

                # get the organization corresponding to the pk and add them to the profile's pinned
                new_organization = Organization.objects.filter(pk=target_org_pk)

                if new_organization.exists(): 

                    # exists method requires a query set so an index is used for the matching organization
                    profile.pinned.add(new_organization[0])
                    profile.save()
                    return HttpResponse(status=204)

                else:

                    return JsonResponse({
                    "error":"organization did not match any in the database"

                }, status=400)


    # if the user was trying to access the URL for some other reason redirect them
    elif request.method == "GET":
        return HttpResponseRedirect(reverse("index"))

# view that updates a volunteer bid when the user submits the form at the bottom of the project
@login_required(login_url= 'sign_in')
def ProjectBidView(request):

    if request.method == "POST":
        
        # look at the data the form submitted and get the corresponding objects
        target_event_id = request.POST["target-event"]
        event_status = request.POST["event-status"]

        if target_event_id is not None and event_status is not None:

            current_profile = Profile.objects.get(pk=request.user.pk)
            target_event = Event.objects.get(pk=target_event_id)

            matching_bids = Bid.objects.filter(event=target_event, bidder=current_profile)

            if event_status == 'volunteered':

                # if the person is volunteering see if they have already volunteered on the server side               
                if not matching_bids.exists():

                    print("no matching bid exists")

                    # if the person is a new volunteer create the bid
                    new_bid = Bid.objects.create(event=target_event, bidder=current_profile)
                    new_bid.save()

            elif event_status == "not_volunteered":

                # if the person is unvolunteering see if they never volunteered in the first place
                if matching_bids.exists():          
            
                    # if the person is unvolunteering then find their bid instance and delete it
                    matching_bids[0].delete()
    
        # redirect to the dashboard that deals with all your volunteers
        return (HttpResponseRedirect(reverse('your_project_view')))

    # if some sort of other request was made to the url redirect to the home page
    return (HttpResponseRedirect(reverse('index')))

            


    
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