from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("apis.urls")),
]

if settings.DEBUG:
    import debug_toolbar 
    urlpatterns += [
        path('silk/', include('silk.urls', namespace='silk')), 
        path('__debug__/', include(debug_toolbar.urls))
    ]