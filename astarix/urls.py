from . import views
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    path('', views.index),
    path('api/map', views.GameMapAPIView.as_view(), name='map_list'),
    path('api/pixel', views.PixelAPIView.as_view(),name='pixel_list'),
    path('api/map/<int:map_id>',views.handle_with_game_map_by_id,name='get_by_id'),
    path('api/pixel/<int:pixel_id>',views.handle_with_pixel_by_id,name='get_by_id'),
    path('api/login', views.LoginAPI.as_view(),name='login'),
    path('api/v1/register',views.RegisterAPI.as_view(),name='register'), # KNOX usa essa
    path('api/v2/register',views.RegisterAPIwithJWT.as_view(),name='register'),  # JWT
    path('api/logout',knox_views.LogoutView.as_view(),name='knox_logout'),
   
]