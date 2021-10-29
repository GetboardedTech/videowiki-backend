from .extract_desc import get_desc
import os

def get_txt_text(inputFileName):
    file = open(inputFileName, "r")
    text = file.read()
    text = text.replace('\n' , '')
    text = ' '.join(text.split())
    title = None
    return text, title

def get_txt_data(inputFileName, file_name):
    text, title = get_txt_text(inputFileName)
    desc = get_desc(text)
    # print(desc)
    d = {}
    d['text'] = text
    d['desc'] = desc
    d['title'] = title
    return d
