# Code from LateefLab and StackOverflow for adding a middleware 
import pytz

from django.utils import timezone

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:

            # try to use the user's timezone else default to UTC
            try:
                timezone.activate(pytz.timezone(tzname))
            except:
                timezone.activate(pytz.timezone('UTC'))
        else:
            timezone.deactivate()
        return self.get_response(request)