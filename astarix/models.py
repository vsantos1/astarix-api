from django.db import models
from uuid import uuid4
# Create your models here.

class Album(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    release_date = models.DateField(auto_now=False, auto_now_add=True)
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)

    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    music = models.FileField(upload_to='songs/')

    def __str__(self):
        return self.name