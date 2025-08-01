import hashlib

from django.core.mail import send_mail
from django.conf import settings
from urllib.parse import urlencode

def send_email(subject, message, email):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    

def get_gravatar_url(email, size=80, default='identicon'):
    email_hash = hashlib.md5(email.lower().strip().encode('utf-8')).hexdigest()
    params = {'s': str(size), 'd': default, 'r': 'pg'}
    query_string = urlencode(params)
    return f"https://www.gravatar.com/avatar/{email_hash}?{query_string}"