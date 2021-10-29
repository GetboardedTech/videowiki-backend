import docx                    # pip install python-docx
import zipfile                 # pip install zipfile
# import shutil

from coutoEditor.global_variable import BASE_URL,BASE_DIR
import os
from .extract_desc import get_desc

def get_doc_text(inputFileName):
    doc = docx.Document(inputFileName)
    all_paras = doc.paragraphs
    d={}
    string = ''
    for para in all_paras:
        s = para.text
        s = s.replace('\n' , '')
        s = ' '.join(s.split())
        string+=s+"\n"
    answer = ''
    for i in range(len(string)-1):
        if string[i]=='\n' and string[i+1]=='\n':
            pass
        else:
            answer+=string[i]
    title = None
    return answer , title

def get_doc_images(inputFileName, file_name):
    if file_name[:-4]=='.doc':
        file_name = file_name[:-4]
    else:
        file_name = file_name[:-5]
    dir = f"media/extract_file/doc_file/{file_name}/"
    folder_name = os.path.join(BASE_DIR,dir)
    folder_url = os.path.join(BASE_URL, dir)
    try:
        os.makedirs(folder_name)
    except OSError:
        pass
    doc = zipfile.ZipFile(inputFileName)
    images = []
    for info in doc.infolist():
        if info.filename.endswith((".png", ".jpeg", ".jpg", ".gif")):
            doc.extract(info.filename, folder_name)
            # shutil.copy(folder_name+"\\"+info.filename, folder_name+"\\"+ inputFileName.split("\\")[-1] + info.filename.split("/")[-1])
            s = os.path.join(folder_name,info.filename)
            image_url = os.path.join(folder_url,info.filename)
            images.append(image_url)
    doc.close()
    return images

def get_doc_data(inputFileName, file_name):
    text, title = get_doc_text(inputFileName)
    images = get_doc_images(inputFileName, file_name)
    desc = get_desc(text)
    d = {}
    d['text'] = text
    d['desc'] = desc
    d['title'] = title
    d['images'] = images
    return d


