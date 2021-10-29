from odf import text, teletype
from odf.opendocument import load
import zipfile
import os
from coutoEditor.global_variable import BASE_URL,BASE_DIR

from .extract_desc import get_desc

def get_odt_text(inputFileName):
    textdoc = load(inputFileName)
    title = textdoc.getElementsByType(text.Title)
    allparas = textdoc.getElementsByType(text.P)
    string = ''
    for i in range(len(allparas)):
        s = teletype.extractText(allparas[i])
        s = s.replace('\n' , '')
        s = ' '.join(s.split())
        string+=s+"\n"
    answer = ''
    for i in range(len(string)-1):
        if string[i]=='\n' and string[i+1]=='\n':
            pass
        else:
            answer+=string[i]
    return answer, title

def get_odt_images(inputFileName, file_name):
    file_name = file_name[:-4]
    dir = f"media/extract_file/odt_file/{file_name}/"
    folder_name = os.path.join(BASE_DIR,dir)
    folder_url = os.path.join(BASE_URL, dir)
    try:
        os.makedirs(folder_name)
    except OSError:
        pass
    odt = zipfile.ZipFile(inputFileName)
    images = []
    for info in odt.infolist():
        if info.filename.endswith((".png", ".jpeg", ".jpg", ".gif")):
            odt.extract(info.filename, folder_name)
            image_path = os.path.join(folder_name,info.filename)
            image_url = os.path.join(folder_url,info.filename)
            images.append(image_url)
    odt.close()
    return images

def get_odt_data(inputFileName, file_name):
    text, title = get_odt_text(inputFileName)
    images = get_odt_images(inputFileName, file_name)
    desc = get_desc(text)
    # print(desc)
    d = {}
    d['text'] = text
    d['desc'] = desc
    d['title'] = title
    d['images'] = images
    return d

