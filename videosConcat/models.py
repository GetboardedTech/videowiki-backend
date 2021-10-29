# from django.db import models
# from user.models import User
# # Create your models here.
#
# class Concatenated_Video(models.Model):
#     thumbnail = models.ImageField(upload_to='concatenated-videos/thumbnail')
#     time = models.DateTimeField(auto_now_add=True, blank=True)
#     video = models.FileField(upload_to='concatenated-videos/video/%Y/%m/%d',blank=False, null=False)
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#
#     def __str__(self):
#         return str(self.video.url)