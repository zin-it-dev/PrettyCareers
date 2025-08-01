from django.db import models
from django.conf import settings
from django.utils.text import slugify

class AuditMixin(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, help_text='Timestamp when the record was created')
    date_modified = models.DateTimeField(auto_now=True, help_text='Timestamp when the record was last updated')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created_by',
        editable=False
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_modified_by',
        editable=False
    )
    
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if 'user' in kwargs:
            user = kwargs.pop('user')
            if not self.pk:
                self.created_by = user
            self.modified_by = user
        
        super().save(**kwargs)
    

class SlugMixin(models.Model):
    slug = models.SlugField(default='', db_index=True, null=False, blank=True, help_text="A short label, generally used in URLs.")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class StatusMixin(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='Active')
    
    class Meta:
        abstract = True
        
        
from rest_framework import serializers
        
class ModelSerializerMixin(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'slug', 'is_active']
        read_only_fields = ['is_active', 'slug']
        
        
class TagSerializer(ModelSerializerMixin):
    tags = serializers.StringRelatedField(many=True)
    
    class Meta:
        fields = ModelSerializerMixin.Meta.fields + ['tags']
        read_only_fields = ModelSerializerMixin.Meta.read_only_fields + ['tags']
        
        
from django.contrib import admin

from .paginatiors import SmallResultsSetPagination

class ModelAdminMixin(admin.ModelAdmin):
    list_per_page = SmallResultsSetPagination.page_size
    list_display = ['is_active', 'date_created', 'date_modified']