from .models import GameMap, Pixel
from rest_framework import serializers
from django.contrib.auth.models import User

class GameMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameMap
        fields = ('id', 'name', 'map_image', 'game')

class PixelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pixel
        fields = ('id', 'title', 'description', 'agent', 'approved','sent_by','game_map','video')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','is_superuser','first_name','last_name')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','is_superuser','first_name','last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user