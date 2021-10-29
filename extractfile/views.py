from rest_framework.views import APIView
from extractfile.working_api.extract_text import extract_text_from_file, extract_data_from_url
from extractfile.working_api.url_to_download import url_download
from videos.models import TemporaryFiles
from datetime import datetime
from django.core.files import File
from django.http import JsonResponse
from rest_framework import status


class ExtractDetailFromUrl(APIView):

    def post(self, request):
        url = request.data['url']

        file_format = ['.pdf', '.ppt', 'pptx', '.doc', 'docx', '.txt', '.odt']
        is_sharepoint = False
        if url.find('sharepoint') != -1:
            is_sharepoint = True
        if url[-4:] in file_format or is_sharepoint == True:
            extension = url.split(".")[-1]
            if is_sharepoint == True:
                extension = request.data['ext']
            temp_file_url, file_name = url_download(url,extension)
            generated_file = open(temp_file_url, "rb")
            file = TemporaryFiles.objects.create(
                temp_file=File(generated_file, name=file_name), created_at=datetime.utcnow()
            ).temp_file
            generated_file.close()
            file1 = str(file)
            print(file1)
            file_data = extract_text_from_file(file)
        else:
            file_data = extract_data_from_url(url)

        return file_data


class ExtractDetailFromFile(APIView):

    def post(self, requests):
        file = TemporaryFiles.objects.create(temp_file=requests.data.get("file", None)).temp_file
        file1 = str(file)
        file_format = ['.pdf', '.ppt', 'pptx', '.doc', 'docx', '.txt', '.odt']
        if file1[-4:] in file_format:
            file_data = extract_text_from_file(file)
            return file_data
        else:
            return JsonResponse({'status': 'false', 'message': 'Invalid Format'}, status=status.HTTP_406_NOT_ACCEPTABLE)
