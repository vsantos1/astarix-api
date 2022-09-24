from django.contrib import admin
from .models import GameMap,Pixel
# Register your models here.

class AdminMap(admin.ModelAdmin):
    list_display = ('name', 'map_image','game')
    search_fields = ('name','game')
    list_filter = ('name','game')
    list_per_page = 10
class AdminPixel(admin.ModelAdmin):
    list_display = ('title','agent','sent_by','game_map','video','approved')
    search_fields = ('title','agent','sent_by','game_map')
    list_filter = ('title','agent','sent_by','game_map')
    list_per_page = 10

admin.site.register(GameMap, AdminMap)
admin.site.register(Pixel,AdminPixel)