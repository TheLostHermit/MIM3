from django import forms

# These forms are properties of models and therefore will cause circular dependency if placed in the form file:

# form to search for a list of volunteers based on their event and status
class VolunteerSearchForm(forms.Form):

    # adding parameter of event choices to the choicefield of the form since they will depend on the project
    def __init__(self, event_choices, *args, **kwargs):

        super(VolunteerSearchForm, self).__init__(*args, **kwargs)
        self.fields["event"].choices = event_choices

    # choices for the volunteers (passed is not included since 'passed' applies to all people once event date passes)
    STATUS_OPTIONS = [
        ('PE', 'Pending'),
        ('AC', 'Accepted'),
        ('DN', 'Denied'),
        ('AA', 'All')
    ]
    # form fields
    event = forms.ChoiceField(choices=(), required=True)
    status = forms.ChoiceField(choices=(STATUS_OPTIONS), required=True)

# radio form for a Bid to determine whether a participant/volunteer is pending, accepted or denied
class StatusForm(forms.Form):

    STATUS_OPTIONS = [
        ('PE', 'Pending'),
        ('AC', 'Accepted'),
        ('DN', 'Denied'),
    ]

    # creates a radio form with status options
    status = forms.ChoiceField(
        choices=STATUS_OPTIONS,
        widget=forms.RadioSelect
        )