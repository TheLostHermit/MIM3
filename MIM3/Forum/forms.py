from django import forms
from django.forms import ModelForm, modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import *

# making forms crispy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit,MultiWidgetField, Fieldset, Button

# form used to create a new profile
class NewProfileForm(UserCreationForm):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'birthday', 'email', 'biography', 'password1', 'password2']

        THIS_YEAR = timezone.now().year

        widgets = {
            "email" : forms.EmailInput(attrs={'class':'form-control'}),
            "birthday" : forms.SelectDateWidget(attrs={'class':'form-control'}, years=reversed(range(1900, THIS_YEAR))),
            "biography" : forms.Textarea(attrs={'class':'form-control'}),
            "password1" : forms.PasswordInput(attrs={'class':'form-control'}),
            "password2" : forms.PasswordInput(attrs={'class':'form-control'})            
        }

    def __init__(self, *args, **kwargs):
        super(NewProfileForm, self).__init__(*args, **kwargs)

        # for some reason if you reload the form the widget clears this selection field
        self.fields['birthday'].widget.years = reversed(range(1900, timezone.now().year))

        self.helper = FormHelper(self)
        self.helper.label_class = 'form-label'
        self.helper.layout = Layout(

            Field('username', css_class="form-control mt-2 mb-3"),
            Fieldset(
                'Enter your name',
                Div('first_name', 'last_name', css_class='input-group')
            ),
            
            MultiWidgetField('birthday', attrs=({'style': 'width: 33%; display: inline-block;'})),
            Field('email'),
            Field('biography'),
            Field('password1', css_class='form-control'),
            Field('password2', css_class='form-control')
        )

        self.helper.form_tag = False
        self.helper.disable_csrf = True

        self.helper.add_input(Submit('Create Account', 'Create Account') )
# form to create a new post or project
class NewPostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'is_project']

# form to add a variable number of images to a post/project
class ImageForm(ModelForm):

    class Meta:

        model = PostImage
        fields = ['name', 'is_icon', 'image']

ImageFormset = modelformset_factory(
    PostImage, form=ImageForm,
)

# form to add a variable number of events to a project
class EventForm(ModelForm):

    date= forms.DateField(localize=True, initial=timezone.now(), widget=forms.SelectDateWidget(years=range(timezone.now().year, timezone.now().year + 10)),)
    time= forms.TimeField(localize=True, initial=timezone.now(),widget=forms.TimeInput(format='%H:%M'))

    class Meta:

        model = Event
        fields = ['date', 'time']
        error_messages = {"min_value" : "This date must not be in the past"}

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.label_class = 'form-label'
        self.helper.layout = Layout(
            
            MultiWidgetField('date', attrs=({'style': 'width: 33%; display: inline-block;'})),
            Field('time', css_class='form-control'),   
        )

        #self.helper[0:3].wrap(Div, css_class="input-group")

        self.helper.form_tag = False
        self.helper.disable_csrf = True
    
        
EventFormset = modelformset_factory(
    Event, EventForm
)

class MessageForm(ModelForm):

    class Meta:

        model = Message
        fields = ['content']

class UpdateProfileForm(ModelForm):

    class Meta:

        model = Profile
        fields = ['username','first_name', 'last_name', 'birthday', 'email', 'biography',]

        widgets = {
            "email" : forms.EmailInput(attrs={'class':'form-control'}),
            "birthday" : forms.SelectDateWidget(attrs={'class':'form-control'}, years=reversed(range(1900, timezone.now().year))),
            "biography" : forms.Textarea(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)

        # for some reason if you reload the form the widget clears this selection field
        self.fields['birthday'].widget.years = reversed(range(1900, timezone.now().year))

        self.helper = FormHelper(self)
        self.helper.label_class = 'form-label'
        self.helper.layout = Layout(

            Field('username', css_class="form-control mt-2 mb-3"),
            Fieldset(
                'Your Name',
                Div('first_name', 'last_name', css_class='input-group')
            ),
            
            MultiWidgetField('birthday', attrs=({'style': 'width: 33%; display: inline-block;'})),
            Field('email'),
            Field('biography'),
        )

        self.helper.add_input(Submit('Change Account', 'Change Account') )