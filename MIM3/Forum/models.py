from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# validators
from django.core.validators import MinValueValidator

# Create your models here.

# Model holding information on an organization
class Organization(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    about = models.TextField(null=False, blank=False)
    logo = models.ImageField(null=True, blank=True)

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
    timestamp = models.DateTimeField(default = timezone.now, blank=True, null=True)
    is_project = models.BooleanField(default=False, null=False, blank=False)

    # organization will be pulled from the author of the post naturally
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='written_posts')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, related_name='our_posts')

    def __str__(self):

        type = self.is_project and "Project" or "Post"
        return f"{type} : {self.title}"

# associates dates and times with posts (projects) so that users can volunteer to participate
class Event(models.Model):
    date = models.DateField(default=timezone.now, null=True, blank=True, validators=[MinValueValidator(timezone.now, "valid values are not in the past")])
    time = models.TimeField(default=timezone.now, null=True, blank=True)
    open = models.BooleanField(default=True, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='project_times')

    def __str__(self):
        return f"Event from {self.project}"

# multiple images can be used for one post. Is icon determines whether the image can be used in the project display
class PostImage(models.Model):

    image = models.ImageField
    name = models.CharField(max_length=100, default="image")
    is_icon = models.BooleanField(default=False, null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='related_images')

    def __str__(self):
        return f"Image '{self.name}' for {self.post.title}"

# short form messages which can be used to send basic information to participants
class Message(models.Model):
    content = models.TextField(null=False, blank=False)
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="sent_messages")
    sending_org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, related_name="sent_messages")
    recipient = models.ManyToManyField(Profile, related_name='received_messages')
    timestamp = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        timestring = self.timestamp.strftime("%d/%m/%Y | %H : %M")
        return f"Message at {timestring} from {self.sender} of {self.sending_org}"

# model linking volunteers to events they want to volunteer for
class Bid(models.Model):

    STATUS_OPTIONS = [
        ('PE', 'Pending'),
        ('AC', 'Accepted'),
        ('DN', 'Denied'),
        ('CP', 'Complete')
    ]

    bidder = models.OneToOneField(Profile, on_delete=models.CASCADE)
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_OPTIONS, default=STATUS_OPTIONS[0][0])

    def __str__(self):
        return f"{self.bidder.username}'s bid on {self.event.post.title}"