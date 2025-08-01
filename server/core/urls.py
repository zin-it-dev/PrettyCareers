from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path(
        "admin/password-reset/",
        auth_views.PasswordResetView.as_view(
            extra_context={"site_header": admin.site.site_header}
        ),
        name="admin_password_reset",
    ),
    path(
        "admin/password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            extra_context={"site_header": admin.site.site_header}
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            extra_context={"site_header": admin.site.site_header}
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            extra_context={"site_header": admin.site.site_header}
        ),
        name="password_reset_complete",
    ),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    
    re_path(r'^', include('apis.urls')),
    
    path('openapi/', SpectacularAPIView.as_view(), name='schema'),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG and not settings.TESTING:
    import debug_toolbar 
    urlpatterns += [
        path('silk/', include('silk.urls', namespace='silk')), 
        path('__debug__/', include(debug_toolbar.urls))
    ]