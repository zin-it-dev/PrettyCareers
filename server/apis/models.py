from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.utils.translation import gettext_lazy as _

from .mixins import StatusMixin, AuditMixin, SlugMixin
from .managers import UserManager
from .utils import get_gravatar_url


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        STUDENT = 'STUDENT', _('Student')
    
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT, verbose_name=_('Role'))
    email = models.EmailField(unique=True, 
        verbose_name=_('Email Address'),
        error_messages={
            'unique': _('A user with that email already exists.'),
        })
    avatar = models.ImageField(upload_to='avatars/%y/%m/%d', 
        null=True, blank=True, 
        storage=MediaCloudinaryStorage(), 
        verbose_name=_('Avatar'),
        help_text=_('Upload your profile picture.'))
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.get_full_name() or self.username or self.email
    
    def save(self, *args, **kwargs):
        self.email = self.__class__.objects.normalize_email(self.email)
        if not self.avatar:
            self.avatar = get_gravatar_url(self.email)
        super().save(*args, **kwargs)
    
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'STUDENT'})

    def __str__(self):
        return self.user.get_full_name()
    
    
class Category(StatusMixin, SlugMixin, AuditMixin):
    name = models.CharField(unique=True, max_length=80)
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name
    

class Tag(StatusMixin, SlugMixin, AuditMixin):
    name = models.CharField(unique=True, max_length=80)
    
    def __str__(self):
        return f"#{self.name}"
    
    
class Base(StatusMixin, SlugMixin, AuditMixin):
    tags = models.ManyToManyField(
            Tag, 
            related_name="%(app_label)s_%(class)s_related",
            related_query_name="%(app_label)s_%(class)ss",
            blank=True
        )
    
    class Meta:
        abstract = True
        
        
class Course(Base):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    name = models.CharField(unique=True, max_length=255)
    price = models.FloatField(default=0.00)
    # description = models.TextField()
    
    def __str__(self):
        return self.name