from django.contrib import admin
from .models import Video,Tags,Scenes
# Register your models here.

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id','title',)

@admin.register(Scenes)
class ScencesAdmin(admin.ModelAdmin):
    list_display = ('id','video',)

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id',)