from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Album, Song
from rest_framework.views import APIView
from .serializers import AlbumSerializer, SongSerializer,RegisterSerializer
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


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class     = RegisterSerializer
    queryset = get_user_model().objects.all()

class AlbumList(APIView):

    #permission_classes = (IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)

    def get_object(self,album_id):
        try:
            return Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            return None

    def get(self,request):
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,album_id):
        album = self.get_object(album_id)
        serializer = AlbumSerializer(album,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_200_OK)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,album_id):
        album = self.get_object(album_id)

        if album == None:
            return Response(status.HTTP_503_SERVICE_UNAVAILABLE)

        album.delete()
        return Response(status.HTTP_204_NO_CONTENT)

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


def index(request):
    return render(request,'index.html')

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_by_id(request,album_id):
   
    err = HandleWithCustomExceptions(status.HTTP_404_NOT_FOUND,
    "Não foi encontrado nenhum album para esse ID",
    f'api/album/{album_id} não encontrado')

    if request.method == 'GET':
        try:
            album = Album.objects.get(id=album_id)
            serializer = AlbumSerializer(album)
            return Response(serializer.data)
        except Album.DoesNotExist:
            return err.handle_with_404_error()

    return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)