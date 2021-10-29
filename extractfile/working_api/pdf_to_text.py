import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

import PyPDF2

import fitz
from PIL import Image

from coutoEditor.global_variable import BASE_URL,BASE_DIR
import os
from .extract_desc import get_desc

def get_pdf_text(inputFileName):
    with open(inputFileName, 'rb') as fh:
        string = ''
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            resource_manager = PDFResourceManager()
            fake_file_handle = io.StringIO()
            converter = TextConverter(resource_manager, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)
            s = fake_file_handle.getvalue()
            s = s.replace('\n' , '')
            s = ' '.join(s.split())
            string+=s+"\n"
            converter.close()
            fake_file_handle.close()
    answer = ''
    for i in range(len(string)-1):
        if string[i]=='\n' and string[i+1]=='\n':
            pass
        else:
            answer+=string[i]
    pdf_obj = open(inputFileName, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdf_obj)
    title = pdfReader.getDocumentInfo().title
    pdf_obj.close()
    return answer, title

def get_pdf_images(inputFileName, file_name):
    file_name=file_name[:-4]
    pdf_file = fitz.open(inputFileName)
    dir = "media/extract_file/pdf_file/"
    folder_name = os.path.join(BASE_DIR, dir)
    folder_url = os.path.join(BASE_URL, dir)
    try:
        os.makedirs(folder_name)
    except OSError:
        pass
    # print(folder_name)
    count = 1
    images=[]
    for page_index in range(len(pdf_file)):
        page = pdf_file[page_index]
        image_list = page.getImageList()
        for image_index, img in enumerate(page.getImageList(), start=1):
            xref = img[0]
            base_image = pdf_file.extractImage(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image = Image.open(io.BytesIO(image_bytes))
            image.save(open(f"{folder_name}{file_name}{count}.{image_ext}", "wb"))
            s = file_name+str(count)+'.'+image_ext
            image_url = os.path.join(folder_url,s)
            images.append(image_url)
            count+=1
    return images

def get_pdf_data(inputFileName, file_name):
    text, title = get_pdf_text(inputFileName)
    images = get_pdf_images(inputFileName, file_name)
    desc = get_desc(text)
    d = {}
    d["text"] = text
    d["desc"] = desc
    d["title"] = title
    d["images"] = images
    return d

