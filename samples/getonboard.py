import os
import sys 
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from scraper.general import GeneralScraper

def build_data_for_scrape_item(item):
    return {  'url': 'https://www.getonbrd.com.pe'+ item.select_one('a')['href'] }

if __name__ == '__main__':
    url = 'https://www.getonbrd.com.pe/empleos/programacion'

    s = GeneralScraper(url, { 
        'hasCategories': False, 
        'selectorCategories': '#ficha-columnistas article.pad-none h4 a',
        'prefixToCategory': '',
        'hasItems': True, 
        'hasPagination': False, 
        'selectorPagination': '.paginacion',
        'selectorItems': '.job' } )

    s.set_callback_build_data_item(build_data_for_scrape_item)
    s.set_map_selector_values({
        'fields': { 
            'title': {'type': 'text', 'specification' : { 'path':'.gb-landing-cover__title' }},

        }
    })
    s.run()

