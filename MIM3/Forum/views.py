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

# utility imports
from datetime import date, time
import re

# importing models and forms from other files in this folder
from .forms import * # models and property forms are imported through this as well

# the number of list items to display before pagination is controlled by this global variable
PAGINATE_NO = 5

# in the case of permission required the user is actually redirected to the index
# view used to create new posts
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

                    if ('image' in form.changed_data):

                        image = form.save(commit=False)
                        image.post = new_post
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

# view that renders a list of images in the post so that they can be deleted/added
class ManagePostImgsView(ListView):

    model = PostImage

    # overriding default template path
    template_name = "Forum/post_pages/mng_post_imgs.html"

    def get_queryset(self, *args, **kwargs):

        queryset = super(ManagePostImgsView, self).get_queryset(*args, **kwargs)

        # return the queryset filtered by the current post        
        current_post = Post.objects.get(pk=self.kwargs['post_pk'])
        return queryset.filter(post=current_post)

    # adding a form to create new images to this context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = ImageForm()
        context['post_pk'] = self.kwargs['post_pk']

        return context

# view that renders  list of events for a project so that they can be added/deleted/changed
class ManageEventsView(ListView):

    model = Event

    # overriding default template path
    template_name = "Forum/post_pages/mng_events.html"

    def get_queryset(self, *args, **kwargs):

        # lists all the events of the post in question
        queryset = super(ManageEventsView, self).get_queryset(*args, **kwargs)
        current_post = Post.objects.get(pk=self.kwargs['post_pk'])
        return queryset.filter(post=current_post)

    # uses the event form for all instances where the event is created or changed
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_form'] = EventForm()
        context['post_pk'] = self.kwargs['post_pk']
        return context

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

# view displaying all volunteers needed in a query
class VolunteerListView(ListView):

    model = Bid

    # overriding default template path (change)
    template_name = "Forum/mngmt_pages/participant_list.html"

    def get_queryset(self, *args, **kwargs):

        queryset = super(VolunteerListView, self).get_queryset(*args, **kwargs)
        target_event = Event.objects.get(pk=self.kwargs['event_pk'])
        target_status = self.kwargs['status']

        # if all participants are being targeted just return all for the event
        if target_status == "AA":
            return queryset.filter(event=target_event)

        else:
            return queryset.filter(status=target_status, event=target_event)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        mail_string = ""
        bid_ids = []
        bidder_ids = []

        for bid in self.get_queryset():
            mail_string += (f"{bid.bidder.email}, ") 
            bid_ids.append(bid.pk)
            bidder_ids.append(bid.bidder.pk)

        # NB: there are probably better ways to pass the IDs of all elements
        # in the list view to other views
        context['mail_list'] = mail_string
        context['bid_ids'] = bid_ids
        context['bidder_ids'] = bidder_ids
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
   
# view that updates images when a user adds or deletes images from a post
@permission_required('Forum.can_post', login_url= 'index')
def ChangeImgView(request, post_pk):

    current_posts = Post.objects.filter(pk=post_pk)

    if current_posts.exists():

        current_post = current_posts[0]

        # when a user deletes an image they use a put request
        if request.method == "PUT":

            data = json.loads(request.body)

            if data.get('img_pk') is not None:

                target_img_pk = data['img_pk']
                target_img_filter = PostImage.objects.filter(pk=target_img_pk)

                # the exist method can only be used on a filter so once its existence is confirmed the 
                # target is the first element of this query
                if target_img_filter.exists():

                    target_img = target_img_filter[0]

                    # if the image is being deleted
                    if data.get('delete') is not None:

                        target_img[0].delete()
                        return HttpResponse(status=204)

                    # if the image's icon status is being changed
                    if data.get('icon_status') is not None:

                        target_img.is_icon = data['icon_status'] == "true" and True or False
                        target_img.save()
                        return HttpResponse(status=204)

            return JsonResponse({
                "error":"Image data was not valid"
            }, status=400)

        # when a user creates an image they use a post request
        elif request.method == "POST":

            new_image_form = ImageForm(request.POST, request.FILES)
            
            if new_image_form.is_valid() and ('image' in new_image_form.changed_data):

                image = new_image_form.save(commit=False)
                image.post = current_post
                image.save()

            # takes you back to the editing view
            return HttpResponseRedirect(reverse('manage_imgs', kwargs={'pk':current_post.pk}))


    return HttpResponseRedirect(reverse('index'))

@permission_required('Forum.can_post', login_url= 'index')
def ChangeEventView(request):

    if request.method == "POST":

        new_event_form = EventForm(request.POST)
        post_id = request.POST["post-id"]

        target_post_filter = Post.objects.filter(pk=post_id)

        if target_post_filter.exists():

            target_post = target_post_filter[0]

            if new_event_form.is_valid():

                new_event = new_event_form.save(commit=False)
                new_event.post = target_post
                new_event.save()

                # if this post is not yet a project then make it so
                if not target_post.is_project:
                    target_post.is_project = True
                    target_post.save()

                # takes you back to the editing view
                return HttpResponseRedirect(reverse('manage_events', kwargs={'post_pk':target_post.pk}))


    elif request.method == "PUT":

        data = json.loads(request.body)

        if data.get('target_event') is not None and data.get('action') is not None:

            target_event_filter = Event.objects.filter(pk=data['target_event'])

            if target_event_filter.exists():

                target_event = target_event_filter[0]
                action = data['action']

                if action == "delete":
                    
                    # if the event is being deleted see whether this is the last event in the project, and if so make it a post
                    if data.get('target_post') is not None:

                        target_post_filter = Post.objects.filter(pk=data['target_post'])

                        if target_post_filter.exists():

                            target_post = target_post_filter[0]
                            
                            total_events = target_post.project_times.count()
                            print(f"total events: {total_events}")
                            
                            if total_events == 1:
                                target_post.is_project = False
                                target_post.save()

                            target_event.delete()
                            return HttpResponse(status=204)

                elif action == "toggle_open":

                    # if the "open" status of the event is being changed (once the new value came through)
                    if data.get('open') is not None:

                        # if the event is closed close the event
                        if data['open'] == "false":

                            target_event.open = False
                            

                        elif data['open'] == "true":

                            target_event.open = True

                        # if the open value is neither of these return an error
                        else:

                            return JsonResponse({
                            "error":"the value of 'open' must be either true or false"
                            }, status=400)

                        # if there was no error save the event and return a successful response    
                        target_event.save()
                        return HttpResponse(status=204)


                elif action == "change":

                    new_time_string = data['new_time']

                    print(new_time_string)
                    
                    # if the new time was left empty
                    if new_time_string == "":

                        new_time_string = str(target_event.time)

                    # this only works in ideal situations when the user has inputted 24hr time with a colon 
                    # between the hours and minutes. Hence by default we only try to make a time out of the 
                    # input
                    new_time_components = new_time_string.split(':')

                    new_hour = int(new_time_components[0])
                    new_minutes = int(new_time_components[1])

                    # try to see if a valid date can be made from the date text input, else reset to current date value
                    try:
                        new_date = date(int(data['new_year']), int(data['new_month']), int(data['new_day']))

                    except:
                        new_date = target_event.date

                    # try to see if a valid time can be made from the time text input, else reset to current time value
                    try:
                        new_time = time(new_hour, new_minutes)

                    except:
                        new_time = target_event.time

                    if (new_date <= date.today()):

                        return JsonResponse({
                            "error":"date is in the past or today"
                        }, status=400)

                    else:

                        target_event.date = new_date
                        target_event.time = new_time
                        target_event.save()
                        return HttpResponse(status=204)                

    # default reverse page if URL was accessed incorrectly (consider making an "error" page)
    return HttpResponseRedirect(reverse('index'))

@permission_required('Forum.can_post', login_url= 'index')
def ViewVolunteersView(request):

    # takes in the form input of the event query and redirects to the listview with the appropriate settings
    if request.method == "POST":

        post_id = request.POST['post_id']
        post_filter = Post.objects.filter(pk=post_id)

        if post_filter.exists():

            event = request.POST[f"{post_id}-event"]
            status = request.POST[f"{post_id}-status"]

            # makes sure the event is valid
            event_filter = Event.objects.filter(pk=event)

            if event_filter.exists():

                return HttpResponseRedirect(reverse('view_volunteers', kwargs={
                    'event_pk':event, 
                    'status': status
                }))

        # else the event no longer exists and re-render this page
        return HttpResponseRedirect(reverse('manage_posts_view'))


def ChangeVolunteerView(request):

    if request.method == "POST":

        # get all the IDs from the bid ID field in the form.
        # this can likely be made better but it's structured this way so that
        # if another person updates the database (eg resigns or volunteers) before the person submitting this form
        # sees the changes the request still has all necessary information to be completed
        bid_list = re.findall(r'\d+',str(request.POST['bid_ids']))

        for bid_id in bid_list:

            bid_filter = Bid.objects.filter(pk=bid_id)
            
            if bid_filter.exists():

                target_bid = bid_filter[0]

                change_form_status = StatusForm(request.POST, prefix=bid_id)

                if change_form_status.is_valid():
                    
                    target_bid.status = change_form_status.cleaned_data['status']
                    target_bid.save()

        return HttpResponseRedirect(reverse('manage_posts_view'))

    # this should eventually become an error page
    return HttpResponseRedirect(reverse('index'))


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