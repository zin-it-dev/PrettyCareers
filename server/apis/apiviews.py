from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from django.conf import settings
from datetime import datetime
from django.middleware import csrf
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import UserSerializer, SetPasswordSerializer, CategorySerializer, CourseSerializer
from .repositories import UserRepository, CategoryRepository, CourseRepository
from .paginatiors import SmallResultsSetPagination, StandardResultsSetPagination, LargeResultsSetPagination
from .filters import CourseFilter


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data["access"]
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=access_token,
            domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
            path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            expires=datetime.utcnow() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        csrf.get_token(request)
        return response


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = UserRepository().get_all()
    serializer_class = UserSerializer
    
    def get_serializer_class(self):
        if self.action == 'set_password':
            return SetPasswordSerializer
        return super().get_serializer_class()
    
    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    
    @action(detail=False, methods=['GET'], url_path='current-user')
    def current_user(self, request):
        return Response(self.get_serializer(request.user).data, status=status.HTTP_200_OK)
    
    
    @action(detail=False, methods=['post'], url_path='set-password')
    def set_password(self, request):
        user = request.user        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
            
            
    @action(detail=False, methods=['GET'], url_path='deactive')
    def deactive_user(self, request):
        user = request.user
        user.is_active = not user.is_active
        user.save()
        return Response(self.get_serializer(user).data, status=status.HTTP_200_OK)
    
    
class CategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = CategoryRepository().get_all()
    serializer_class = CategorySerializer
    
    
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CourseRepository().get_all()
    serializer_class = CourseSerializer
    pagination_class = SmallResultsSetPagination
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = CourseFilter
    search_fields = ['name']
    ordering_fields = ['name', 'price']