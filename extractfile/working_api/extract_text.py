from extractfile.working_api.ppt_to_image import extract_info_from_ppt
from extractfile.working_api.pdf_to_text import get_pdf_data
from extractfile.working_api.docs_to_text import get_doc_data
from extractfile.working_api.txt_to_text import get_txt_data
from extractfile.working_api.odt_to_text import get_odt_data
from extractfile.working_api.url_to_text import get_url_data
from django.http import JsonResponse

from coutoEditor.global_variable import BASE_DIR,BASE_URL
import os

def extract_text_from_file(file):
    file_path = BASE_DIR + str(file.url)
    file_name = str(os.path.basename(file.name))

    if file_path.endswith('ppt') or file_path.endswith('pptx'):
        ppt_data = extract_info_from_ppt(file_path, file_name)
        return  JsonResponse({"status":True,"data":ppt_data})

    elif file_path.endswith("pdf"):
        pdf_data = get_pdf_data(file_path, file_name)
        return  JsonResponse({"status":True,"data":pdf_data})

    elif file_path.endswith('doc') or file_path.endswith('docx'):
        docs_data = get_doc_data(file_path, file_name)
        return  JsonResponse({'status':True,'data':docs_data})
    
    elif file_path.endswith("txt"):
        txt_data = get_txt_data(file_path, file_name)
        return  JsonResponse({'status':True,'data':txt_data})

    elif file_path.endswith("odt"):
        odt_data = get_odt_data(file_path, file_name)
        return  JsonResponse({'status':True,'data':odt_data})

    else:
        return  JsonResponse({'status':False,'data':"file format is invalid"})

def extract_data_from_url(url):
    try:
        # response = requests.get(url)
        url_data = get_url_data(url)
        return  JsonResponse({'status':True,'data': url_data})
    except:
        return  JsonResponse({'status':False,'data':"URL is invalid"})


"""
url_data = {
    "text"  : extracted part first priority
    "images": download or location list ["location1","location2",......]
    "title" : if possible
    "desc"  : description
}
ppt_data = {
   "ppt"  : file location,
   "title": title,
   "desc" : if any
    "slides": {
        0:{"images":file location,"text":text}
        ......
    }
    "images": [location1,location2,........]
}
docs_data = {
    "title" : None
    "text"  : extracted part
    "desc"  : description
    "images": download or location list ["location1","location2",......]
}
pdf_data = {
    "title" : None
    "text"  : extracted part
    "desc"  : description
    "images": download or location list ["location1","location2",......]
}
txt_data = {
    "title" : None
    "text"  : extracted part
    "desc"  : description
    "images": download or location list ["location1","location2",......]
}
odt_data = {
    "title" : title
    "text"  : extracted part
    "desc"  : description
    "images": download or location list ["location1","location2",......]
}
"""
