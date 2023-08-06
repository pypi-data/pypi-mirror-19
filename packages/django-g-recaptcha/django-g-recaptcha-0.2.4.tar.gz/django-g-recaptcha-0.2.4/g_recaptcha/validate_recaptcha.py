from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json

from django.http import HttpResponse
from django.conf import settings
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

            data = urlencode(values)
            # The post data must be bytes
            req = Request(url, data.encode('ascii'))
            response = urlopen(req)
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