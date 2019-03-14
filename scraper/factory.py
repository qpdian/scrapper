from scraper.util import format_text, get_date_from_any_format_date, download_file

def create_text(specification, source):
    elementHtml = source.select_one( specification['path'])  
    return  elementHtml.getText() if elementHtml else ''

def create_attribute(specification, source):
    elementHtml = source.select_one( specification['path'])  
    return  elementHtml.get(specification['value'])  if elementHtml else ''

def create_paragraph(specification, source):
    selectors =   specification['path'] if isinstance(specification['path'], list) else [specification['path']]
    value = ''
    for selector in selectors:
        elementHtml =  source.select(selector) 
        textElements = map(lambda p : p.getText(), elementHtml)
        value = value + ''.join(textElements) 
    return format_text(value) 

def create_date(specification, source):
    elementHtml = source.select_one( specification['path'])  
    value = elementHtml.get(specification['value'])  if elementHtml else ''
    return get_date_from_any_format_date(value) 


def handle_download(url, directory):
    file_name = None
    try:
        file_name = download_file(url, directory )
    except Exception as e:
        print(e)    
    return file_name

def get_url_file( specification, source):
    url = ''
    if specification.get('handler'):
        url = specification.get('handler')(source)
    else:
        url = source.get('href') if source else None
    return url

def create_files(specification, source):
    
    if specification.get('multiple'):
        elementHtml =  source.select( specification['path']) 
        filesUrls = list(map( lambda element: get_url_file(specification, element) , elementHtml)) 
    else:
        elementHtml = source.select_one( specification['path'])  
        filesUrls = [get_url_file(specification, elementHtml)] 
    return list( map( lambda url : handle_download(url,specification['directory']), filesUrls ))
   
def create_images(specification, source):
    return ''

constructorRepository = {
    'text': create_text,
    'attribute': create_attribute,
    'paragraph': create_paragraph,
    'date': create_date,
    'files': create_files,
    'images': create_images
}


def loadConstructor(typeConstructor):
    return constructorRepository.get(typeConstructor)

def get_value(typeItem, specification, source):
    constructorChoosed = loadConstructor( typeItem )
    return constructorChoosed(specification, source)
