from django.http import HttpResponse
from django.conf import settings
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import json
from django.shortcuts import render

def validate_captcha(view):
    """
    Decorator to validate a captcha, settings from django

    @validate_Captcha
    def a_view():
        ...
    """

    def wrap(request, *args, **kwargs):

        def failure_http():
            # Status 401 means that they are not authorized
            return render(request, 'captcha_fail.html', status=401)

        def failure_ajax():
            return HttpResponse(
                'There was a problem with the captcha, please try again', status=401)

        if request.method == 'POST':
            url = "https://www.google.com/recaptcha/api/siteverify"
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': request.POST.get('g-recaptcha-response', None),
                'remoteip': request.META.get("REMOTE_ADDR", None),
            }

            data = urllib.parse.urlencode(values)
            req = urllib.request.Request(url, data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read())

            # result["success"] will be True on a success
            if result["success"]:
                return view(request, *args, **kwargs)
            elif request.is_ajax():
                return failure_ajax()
            else:
                return failure_http()

        return view(request, *args, **kwargs)
    wrap._original = view
    return wrap