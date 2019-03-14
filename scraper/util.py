import requests
import os, errno
import shutil 
from urllib.parse import unquote
import string
import dateparser

def format_text(text = ''):
    return text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').replace('\xa0', '')

def get_date_from_any_format_date( text ):
    return  dateparser.parse(text)


def download_image (logger, url, downloadPath):
    try:
        response = requests.get(url, stream=True)
        with open(downloadPath, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
    except Exception:
        logger.custom("Could not download image")
        return None

def generate_filename():
    size = 10
    allchar = string.ascii_letters + string.digits
    name = "".join(choice(allchar) for x in range(randint(size, size)))
    return '_' + name

def download_file(url, downloadPath):
    if not os.path.exists(downloadPath):
        os.makedirs(downloadPath)
    r = requests.get(url, stream=True)

    tmp = downloadPath + url[url.rfind('/') + 1:]
    tmp = unquote(tmp)
    with open(tmp, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: 
                f.write(chunk)   
    new_file = tmp[:tmp.rfind('.')] + generate_filename() + tmp[tmp.rfind('.'):]
    os.rename(tmp, new_file)
    return new_file        



