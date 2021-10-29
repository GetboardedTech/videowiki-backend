from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from .models import TemporaryFiles
from coutoEditor.settings import BASE_URL

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
      file = TemporaryFiles.objects.create(
          temp_file=request.data['media'],
          created_at=datetime.utcnow()
      )
      return Response({"media_url":BASE_URL+file.temp_file.url[1:]},status=status.HTTP_201_CREATED)