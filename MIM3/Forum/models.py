from django.db import models
from django.contrib.auth.models import User
import pytz
from django.utils import timezone
from django.template.defaultfilters import date as format_date
from django.template.defaultfilters import time as format_time

# imports for deleting files from the media folder completely when an object is deleted or changed
from django.db.models.signals import post_delete
from .utils import file_cleanup

# validators
from django.core.validators import MinValueValidator

# forms for properties of models
from .property_forms import *

# Create your models here.

# Model holding information on an organization
class Organization(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    about = models.TextField(null=False, blank=False)
    logo = models.ImageField(null=True, blank=True, upload_to='organization_logos')
    official_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

# Model holding information in a profile
class Profile(User):
    birthday = models.DateField(default=timezone.now, blank=True, null=True)
    biography = models.TextField(default="I am a user of this website", null=True, blank=True)
    pinned = models.ManyToManyField(Organization, related_name="followers",blank=True)
    
    # a profile can only be mapped to one organization at a time so that when sending notices
    # the program knows which organization is responsible for the notice

    membership = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL, related_name='members')

    # permissions for the user: whether the user is allowed to post on behalf of an organization
    class Meta:
        permissions = [
            ("can_post", "can post on behalf of an organization")
        ]

# Model holding information for a post/project
class Post(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_project = models.BooleanField(default=False, null=False, blank=False, verbose_name="Make this a project")

    # organization will be pulled from the author of the post naturally
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='written_posts')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, related_name='our_posts')

    def __str__(self):

        type = self.is_project and "Project" or "Post"
        return f"{type} : {self.title}"

    # adds a property which sends out a form which lets the user filter volunteers by event and type
    @property
    def get_volunteer_search_form(self):

        if self.is_project:

            EVENT_CHOICES = []

            # get all the events of this project
            for event in self.project_times.all():

                if event.open:

                    # using Django's built in date formatting tools
                    date_str = format_date(event.date, "j N Y")
                    time_str = format_time(event.time, 'g:i a')                    
                    EVENT_CHOICES.append((event.pk, f"{date_str} at {time_str}"))

            # technically the form works without the prefix but it results in multiple forms with the same ID
            return VolunteerSearchForm(EVENT_CHOICES, prefix=self.pk)

# associates dates and times with posts (projects) so that users can volunteer to participate
class Event(models.Model):
    date = models.DateField(default=timezone.now, null=True, blank=True, validators=[MinValueValidator(timezone.now().date(), "valid values are not in the past")])
    time = models.TimeField(default=timezone.now, null=True, blank=True)
    open = models.BooleanField(default=True, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='project_times')

    # adds a property to check whether this event has passed and if so change the open status
    @property
    def passed(self):

        if (self.date < timezone.now().date()):
            self.open = False
            return True

        else:
            return False

    # property which returns the formatted date and time of an event at once
    @property
    def datetime(self):

        timezone.activate(timezone.get_current_timezone())

        # using Django's built in date formatting tools
        aware_time = pytz.utc.localize(self.time)
        print(timezone.localtime(aware_time))
        date_str = format_date(self.date, "j N Y")
        time_str = format_time(pytz.utc.localize(self.time), 'g:i O') 

        return f"{date_str} at {time_str}"

    def __str__(self):
        return f"Event from {self.post.title}"

# multiple images can be used for one post. Is icon determines whether the image can be used in the project display
class PostImage(models.Model):

    #
    image = models.ImageField(upload_to='post_images', default='default.png', blank=False)
    name = models.CharField(max_length=100, default="image")
    is_icon = models.BooleanField(default=False, null=False, blank=False, verbose_name="Make icon of post/project")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='related_images')

    def __str__(self):
        return f"Image '{self.name}' for {self.post.title}"

# short form messages which can be used to send basic information to participants
class Message(models.Model):
    content = models.TextField(null=False, blank=False)
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="sent_messages")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, related_name="messages")
    sending_org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, related_name="sent_messages")
    recipient = models.ManyToManyField(Profile, related_name='received_messages')
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        timestring = self.timestamp.strftime("%d/%m/%Y | %H : %M")
        return f"Message at {timestring} UTC from {self.sender} of {self.sending_org}"

# model linking volunteers to events they want to volunteer for
class Bid(models.Model):

    STATUS_OPTIONS = [
        ('PE', 'Pending'),
        ('AC', 'Accepted'),
        ('DN', 'Denied'),
        ('CP', 'Passed')
    ]

    bidder = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='bids')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bids')
    status = models.CharField(max_length=2, choices=STATUS_OPTIONS, default=STATUS_OPTIONS[0][0])

    # a property which will return a radio form for a user to select the current status of the bid
    @property
    def get_status_form(self):
        return StatusForm(initial={"status":self.status}, prefix=self.pk)

    def __str__(self):
        return f"{self.bidder.username}'s bid on {self.event.post.title}"

# deleting old media files from object when the object is deleted (file cleanup)
post_delete.connect(
    file_cleanup, sender=PostImage, dispatch_uid="media.post_images.file_cleanup"
)

post_delete.connect(
    file_cleanup, sender=Organization, dispatch_uid="media.organization_logos.file_cleanup"
)