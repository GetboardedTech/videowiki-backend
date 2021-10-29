from django.db import models
from user.models import User
from django.utils import timezone

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    thumbnail = models.FileField(upload_to='publish/%Y/%m/%d/thumbnail',default=None,null=True)
    video = models.FileField(upload_to='publish/%Y/%m/%d/video',default=None,null=True)
    script = models.TextField(null=True)
    topic = models.CharField(max_length=100, default="Education",null=True)
    rating = models.FloatField(default=0.0,null=True)
    publish_time = models.DateTimeField(default=timezone.datetime.utcnow, blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    is_save_later=models.BooleanField(default=False,blank=True,null=True)
    publised_video_id=models.IntegerField(default=None,null=True)
    language=models.CharField(max_length=5,default="en",null=True)
    duration=models.TimeField(default=timezone.datetime.utcnow,null=True)
    background_music_file=models.FileField(upload_to='publish/%Y/%m/%d/bgm',default=None,blank=True,null=True)
    background_music_url = models.URLField(default=None,null=True,blank=True)

class TemporaryFiles(models.Model):
    created_at=models.DateTimeField(default=timezone.datetime.utcnow)
    temp_file=models.FileField(upload_to="temporary/%Y/%m/%d")

class Tags(models.Model):
    tag=models.CharField(max_length=200,null=True,blank=True)
    videos=models.ManyToManyField(Video)

class Scenes(models.Model):
    order=models.IntegerField(default=1,null=True,blank=True)
    video_url=models.URLField(default=None,null=True,blank=True)
    video_file=models.FileField(upload_to='scenes/user_uploaded_video/%Y/%m/%d',blank=True, null=True)
    text=models.TextField(null=True,blank=True,default="")
    keywords=models.TextField(null=True,blank=True,default="")
    font_color=models.CharField(max_length=10,default="#000000",null=True,blank=True)
    background_color=models.CharField(max_length=10,default="#ffffff",null=True,blank=True)
    text_position=models.CharField(max_length=10,default="bottom",null=True,blank=True)
    narration = models.FileField(upload_to='scenes/user_uploaded_narration/%Y/%m/%d', blank=True, null=True)
    video=models.ForeignKey(Video,on_delete=models.CASCADE,default=None,null=True,blank=True)
