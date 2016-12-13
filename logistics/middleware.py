from django.utils import timezone

from logistics.permissions import is_driver


class UpdateOnlineMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        user = request.user
        if is_driver(user):
            user.driver.last_seen = timezone.now()
            user.driver.save(update_fields=["last_seen"])

        return response