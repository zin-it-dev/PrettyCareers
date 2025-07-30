from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed


def enforce_csrf(request):
    check = CSRFCheck(lambda req: None)
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            header = self.get_header(request)
        
            if header is None:
                raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
            else:
                raw_token = self.get_raw_token(header)
            
            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)
            
            if request.method not in ('GET', 'HEAD', 'OPTIONS'):
                enforce_csrf(request)
            
            return self.get_user(validated_token), validated_token
        except InvalidToken:
            raise AuthenticationFailed('Invalid token provided.')
        except TokenError:
            raise AuthenticationFailed('Error decoding token.')
        except AuthenticationFailed as e:
            raise e
        except Exception as e:
            raise AuthenticationFailed(f'Authentication failed: {e}')