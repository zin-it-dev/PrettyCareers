from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apis.urls")),
    
    path('openapi/', SpectacularAPIView.as_view(), name='schema'),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG and not settings.TESTING:
    import debug_toolbar 
    urlpatterns += [
        path('silk/', include('silk.urls', namespace='silk')), 
        path('__debug__/', include(debug_toolbar.urls))
    ]