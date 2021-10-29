import os
from coutoEditor.global_variable import BASE_DIR
import requests
from django.core.files import File
import uuid
from datetime import datetime


def url_download(
        url,
        extension
):
    filename = str(uuid.uuid4())
    download_path = os.path.join(BASE_DIR, "media/download/")
    if not os.path.exists(os.path.join(BASE_DIR, "media/download/")):
        os.mkdir(os.path.join(BASE_DIR, "media/download/"))
    r = requests.get(url)
    open(download_path + filename + "." + extension, "wb").write(r.content)

    return download_path + filename + "." + extension, filename + "." + extension
    #return download_path + filename + "." + url.split(".")[-1]name=file_name + ".mp4"),
                                               #created_at=datetime.utcnow()
    # local_file = open(download_path + filename + "." + url.split(".")[-1], 'rb')
    # # djangofile = File(local_file)
    # print(File(download_path + filename + "." + url.split(".")[-1]))
    # # print("url dwnld ", file)
    # file = TemporaryFiles.objects.create(
    #     temp_file=File(download_path + filename + "." + url.split(".")[-1], name=file_name + ".mp4")).temp_file
    # print("url dwnld ", file)
    # return filelocal_file = open(download_path + filename + "." + url.split(".")[-1],'rb')
    # # djangofile = File(local_file)
    # print(File(download_path + filename + "." + url.split(".")[-1]))
    # # print("url dwnld ", file)
    # file = TemporaryFiles.objects.create(temp_file=File(download_path + filename + "." + url.split(".")[-1],name=file_name + ".mp4")).temp_file
    # print("url dwnld ", file)
    # return file
    #
