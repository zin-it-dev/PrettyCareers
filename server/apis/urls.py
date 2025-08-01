from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenVerifyView, TokenBlacklistView
from django_rest_passwordreset.urls import add_reset_password_urls_to_router

from .apiviews import UserViewSet, CookieTokenObtainPairView, CategoryViewSet, CourseViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'courses', CourseViewSet, basename='course')

add_reset_password_urls_to_router(router, base_path='auth/passwordreset')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CookieTokenObtainPairView.as_view(), name='token_obtain'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]