import pytz

from django.utils import timezone
from rest_framework_simplejwt import authentication


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = None
        user = self.get_request_user(request)
        if user:
            tzname = pytz.all_timezones[int(user.timezone)]
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)

    def get_request_user(self, request):
        try:
            return authentication.JWTAuthentication().authenticate(request)[0]
        except:
            return None