
import json
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import GameMap, Pixel
from .pagination import CustomPagination
from .serializers import GameMapSerializer, PixelSerializer,RegisterSerializer
from django.contrib.auth import  login
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from knox.views import LoginView as KnoxLoginView
from .exceptions import HandleWithCustomExceptions
from django.db.models import Q
from .filters import PixelFilter,MapFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class     = RegisterSerializer
    queryset = get_user_model().objects.all()

class RegisterAPIwithJWT(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            serializer = RegisterSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                create_account = serializer.save()
                data['response'] = "Usuário criado com sucesso."
                data['email'] = create_account.email
                data['username'] = create_account.username
                data['first_name'] = create_account.first_name
                data['last_name'] = create_account.last_name
                #data['password'] = create_account.password
        
                refresh = RefreshToken.for_user(create_account)
                data['token'] = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    }
                return Response(data,status.HTTP_201_CREATED)
            
            else:
                data = serializer.errors

        return Response(data,status.HTTP_201_CREATED)   
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class GameMapAPIView(generics.ListAPIView):
    queryset = GameMap.objects.all()
    serializer_class = GameMapSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MapFilter
    filterset_fields = ['name','game']
    search_fields = ['name','game']

    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            serializer = GameMapSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
    

class PixelAPIView(generics.ListAPIView):
    queryset = Pixel.objects.all()
    serializer_class = PixelSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = PixelFilter
    pagination_class = CustomPagination 
    filterset_fields = ['title','agent','description','game_map']
    search_fields = ['title','agent','description','game_map']

    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            serializer = PixelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



def does_exists_game_map(map_id):

    try:
        return GameMap.objects.get(id=map_id)
    except GameMap.DoesNotExist:
            return None

def does_exists_pixel(pixel_id):
    try:
        return Pixel.objects.get(id=pixel_id)
    except Pixel.DoesNotExist:
        return None


@api_view(['GET','PUT','DELETE'])
@permission_classes([permissions.IsAuthenticated])
def handle_with_game_map_by_id(request,map_id):
    err_msg = f'api/map/{map_id} não encontrado'
    __err = HandleWithCustomExceptions(err_msg)

    if request.method == 'GET':
        try:
            game_map = GameMap.objects.get(id=map_id)
            serializer = GameMapSerializer(game_map)
            return Response(serializer.data)
        except GameMap.DoesNotExist:
            return __err.handle_with_404_error()

    if request.method == 'PUT':
        mapa = does_exists_game_map(map_id)
        if mapa is None:
            return __err.handle_with_404_error()

        serializer = GameMapSerializer(mapa,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        mapa = does_exists_game_map(map_id)
        
        if mapa is None:
            return __err.handle_with_404_error()

        mapa.delete()
        return Response(status.HTTP_204_NO_CONTENT)



def index(request):
    return render(request,'index.html')



@api_view(['GET','PUT','DELETE'])
@permission_classes([permissions.IsAuthenticated])
def handle_with_pixel_by_id(request,pixel_id):
    
    err_msg = f'api/pixel/{pixel_id} não encontrado'
    __err = HandleWithCustomExceptions(err_msg)
    

    if request.method == 'GET':
        try:
            pixel_obj = Pixel.objects.get(id=pixel_id)
            serializer = PixelSerializer(pixel_obj)
            return Response(serializer.data)
        except Pixel.DoesNotExist:
            return __err.handle_with_404_error()

    if request.method == 'PUT':
        pixel = does_exists_pixel(pixel_id)
        if pixel is None:
            return __err.handle_with_404_error()

        serializer = PixelSerializer(pixel,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        pixel = does_exists_pixel(pixel_id)
        
        if pixel is None:
            return __err.handle_with_404_error()

        pixel.delete()
        return Response(status.HTTP_204_NO_CONTENT) 

         