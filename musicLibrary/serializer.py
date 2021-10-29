from rest_framework import serializers
from .models import MusicLib
from coutoEditor.global_variable import BASE_URL

class MusicLibSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        music_url = f'{BASE_URL[:-1]}{obj.file.url}'
        return music_url

    class Meta:
        model = MusicLib
        fields = ('id','url','genre','title')
