from django.conf import settings
from drf_spectacular.extensions import OpenApiAuthenticationExtension


class CookieJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'apis.authenticate.CookieJWTAuthentication'
    name = 'JWT Cookie Authentication'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'cookie',
            'name': settings.SIMPLE_JWT["AUTH_COOKIE"],
            'description': 'JWT token from HttpOnly Cookie'
        }
