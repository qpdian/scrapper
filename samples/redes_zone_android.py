import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from scraper.general import GeneralScraper


def build_data_for_scrape_item(item):
    return {'url' : item.find('h2', {"class": 'entry-title'}).find('a')['href']}


def callbak_get_next_url( paginationSection ):
    return paginationSection.select('.nextpostslink')[0]['href'] if  len(paginationSection.select('.nextpostslink'))>0  else None

if __name__ == '__main__':
    url = 'https://www.redeszone.net/category/android/'
    header = { 
        ':authority': 'www.redeszone.net',
        ':method': 'GET',
        ':scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': '_ga=GA1.2.192886791.1539100238; _gid=GA1.2.1116396068.1539100238; __gads=ID=e2ab237bc4a4f2ef:T=1539100640:S=ALNI_MZRdbEXOLT6wQMjFYIuj9jCto2QFA; _gat=1; __unam=ac51cfa-1665985e9c4-2ff2193a-44',
        'upgrade-insecure-requests': 1
    }

    s = GeneralScraper(url, { 
        'hasPagination': True, 
        'hasItems': True, 
        'selectorItems': '.news-item',
        'selectorPagination': '.wp-pagenavi' }, header )

    s.set_callback_build_data_item(build_data_for_scrape_item)
    s.set_map_selector_values({
        'pathContainer':'.news-item',
        'fields': { 
            'title': { 'type': 'text', 'specification' : { 'path':'h2 > a' }},
            'description': { 'type': 'paragraph', 'specification' : {'path':'p' }},
            'date': { 'type': 'date', 'specification' : {'path':'time', 'value':'datetime' }},
            'autor': { 'type': 'text', 'specification' : { 'path':'.author > span'  }}
        }
    })
    s.set_callback_get_next_link(callbak_get_next_url)
    s.run()

