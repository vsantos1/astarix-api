"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from astarix.views import UserViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="Spotify API",
      default_version='v1',
      description="Music API based on Spotify",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="email@emai.com"),
      license=openapi.License(name="Jose License"),

   ),
   public=True,
   permission_classes=[permissions.AllowAny],
   authentication_classes=[]
)
urlpatterns = [
    path('', include('astarix.urls')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   # path('api/token',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    #path('api/token/refresh',TokenRefreshView.as_view(),name='token_refresh'),
    path("api/auth-token", obtain_auth_token, name="api_token_auth"),

]

router = DefaultRouter()
router.register('user',UserViewSet,basename='user')
urlpatterns += router.urls