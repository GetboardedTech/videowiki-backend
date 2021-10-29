import requests
from bs4 import BeautifulSoup
from coutoEditor.global_variable import BASE_URL, BASE_DIR
from .extract_desc import get_desc
import os

def get_url_images(url):
    url = str(url)
    url_name=url[-10:]
    res = requests.get(url)
    html_page = res.text
    soup = BeautifulSoup(html_page, 'html.parser')
    images = soup.findAll('img')

    dir = "media/extract_file/url_file/"
    folder_name = os.path.join(BASE_DIR, dir)
    folder_url = os.path.join(BASE_URL, dir)
    try:
        os.makedirs(folder_name)
    except OSError:
        pass

    count = 0
    images_url = []
    for i, image in enumerate(images):
        try:
            image_link = image["src"]
            if '?' in image_link:
                image_link = ''
            else:
                pass
        except:
            pass
        try:
            r = requests.get(image_link).content
            try:
                r=str(r, 'utf-8')
            except UnicodeDecodeError:
                with open(f"{folder_name}{url_name}{count+1}.jpg", "wb+") as f:
                    s = url_name+str(count+1)+'.jpg'
                    image_url = os.path.join(folder_url,s)
                    images_url.append(image_url)
                    f.write(r)
                count+=1
        except:
            pass
        image_link = ''
    return images_url

def get_url_text(url):
    res = requests.get(url)
    html_page = res.text
    soup = BeautifulSoup(html_page, 'html.parser')
    string, get_title = '', ''
    for data in soup.find_all("p"):
        s = data.get_text()
        s = s.replace('\n' , '')
        s = ' '.join(s.split())
        string += s+"\n" + "\n"
    for title in soup.find_all('title'):
        get_title += title.get_text() 
    return string, get_title

def get_url_data(url):
    text, title = get_url_text(url)
    # images = get_url_images(url)
    desc = get_desc(text)
    d={}
    d["text"] = text
    d["title"] = title
    d["desc"] = desc
    d["images"] = None
    return d
