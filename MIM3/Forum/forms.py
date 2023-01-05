from django import forms
from django.forms import ModelForm, modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import *

# form used to create a new profile
class NewProfileForm(UserCreationForm):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'birthday', 'email', 'biography', 'password1', 'password2']

        widgets = {
            "first_name": forms.TextInput(attrs={'class':'form_control'}),
            "last_name" : forms.TextInput(attrs={'class':'form_control'}),
            "username" : forms.TextInput(attrs={'class':'form_control'}),
            "email" : forms.EmailInput(attrs={'class':'form_control'}),
            "birthday" : forms.SelectDateWidget(attrs={'class':'form_control'}, years=reversed(range(1900, timezone.now().year))),
            "biography" : forms.TextInput(attrs={'class':'form_control'}),
            "password1" : forms.PasswordInput(attrs={'class':'form_control'}),
            "password2" : forms.PasswordInput(attrs={'class':'form_control'})            
        }

# form to create a new post or project
class NewPostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'is_project']

# form to add a variable number of images to a post/project
ImageFormset = modelformset_factory(
    PostImage, fields = ('name', 'image', 'is_icon'),
)

# form to add a variable number of events to a project
EventFormset = modelformset_factory(
    Event, fields = ('date', 'time'),

    widgets= {
        "date" : forms.SelectDateWidget(years=range(timezone.now().year, timezone.now().year + 10)),
        "time" : forms.TimeInput(format='%H:%M'),
    },

    error_messages={"min_value" : "This date must not be in the past"},
)