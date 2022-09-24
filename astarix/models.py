from django.db import models
from uuid import uuid4
# Create your models here.

class GameMap(models.Model):
    name = models.CharField(max_length=100)
    map_image = models.ImageField(upload_to='images/')
    game = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Pixel(models.Model):
    title = models.CharField(max_length=100,blank=False)
    description = models.CharField(max_length=255,blank=True)
    agent = models.CharField(max_length=100,blank=False)
    approved = models.BooleanField(default=False)
    sent_by = models.CharField(max_length=100,blank=True)
    game_map = models.ForeignKey(GameMap,on_delete=models.DO_NOTHING)
    video = models.FileField(upload_to='videos/',blank=True)

    def __str__(self):
        return self.title