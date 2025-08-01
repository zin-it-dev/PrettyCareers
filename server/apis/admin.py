from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

from .models import User, Category, Course, Tag
from .mixins import ModelAdminMixin
from .forms import UserChangeForm, UserCreationForm


class CategoryAdmin(ModelAdminMixin):
    list_display = ['name'] + ModelAdminMixin.list_display


class CourseAdmin(ModelAdminMixin):
    list_display = ['name'] + ModelAdminMixin.list_display


class TagAdmin(ModelAdminMixin):
    list_display = ['name'] + ModelAdminMixin.list_display
    


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ["email", "username", "is_active", "role"]
    fieldsets = [
        (None, {"fields": ["username", "email", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name", "avatar"]}),
        ("Permissions", {"fields": ["role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions"]}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["role", "email", "username", "password", "confirm_password", "first_name", "last_name", "avatar", "is_active", "is_staff", "is_superuser"],
            },
        ),
    ]
    search_fields = ["email", "username", "first_name", "last_name"]
    ordering = ["email"]
    filter_horizontal = []
    

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Tag, TagAdmin)