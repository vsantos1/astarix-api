from . import views
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    path('', views.index),
    path('api/album', views.AlbumList.as_view()),
    path('api/album/<int:album_id>',views.get_by_id,name='get_by_id'),
    path('api/login', views.LoginAPI.as_view(),name='login'),
    path('api/v1/register',views.RegisterAPI.as_view(),name='register'), # KNOX
    path('api/v2/register',views.RegisterAPIwithJWT.as_view(),name='register'),  # JWT
    path('api/logout/',knox_views.LogoutView.as_view(),name='knox_logout'),
   
]