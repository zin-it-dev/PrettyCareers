import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

from .models import User, Student
from .utils import send_email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == User.Role.STUDENT:
            Student.objects.create(user=instance)
        elif instance.role == User.Role.ADMIN:
            instance.is_superuser = True
            instance.is_staff = True
            instance.save(update_fields=["is_superuser", "is_staff"])
            

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    reset_url = f"{os.environ.get('CLIENT_BASE_URL')}/reset-password?token={reset_password_token.key}&email={reset_password_token.user.email}"

    send_email(
        subject="🔒 Password Reset Request", 
        message=f"""
            Hello {reset_password_token.user.username},

            We received a request to reset your password.

            Click the link below to reset your password:
            {reset_url}

            If you did not request this, please ignore this email.""", 
        email=reset_password_token.user.email
    )