import os
import time
import requests
import string
from bs4 import BeautifulSoup

from scraper.logger import Logger
from scraper.processor import Processor
from scraper.mapping  import get_result_by_mapping
from scraper.util import format_text


class GeneralScraper:
 
    result = {'items': []}
    mapSelectorValue = None
    callbackGetResult = None
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': '',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
        'X-Requested-With': 'XMLHttpRequest'
    }
 
    def __init__(self, url, config = {}, header = {}):
        self.url = url
        self.config = config
        self.logger = Logger(self)
        self.processor = Processor()

        self.header.update(header) 
    
    def set_callback_build_data_item(self, callback):
        self.callbackBuildDataItem = callback

    def set_callback_get_result(self, callback):
        self.callbackGetResult = callback

    def set_callback_get_next_link(self, callback):
        self.callbackGetNextLink = callback

    def set_map_selector_values(self, mapSelectorValue):
        self.mapSelectorValue = mapSelectorValue
    
    def set_callback_get_children(self, callback):
        self.callbackGetChildren = callback



    def get_response(self, url):
        response = ''
        while response == '':
            try:
                response = requests.get(url)
                break
            except:
                print("Connection refused by the server..")
                time.sleep(5)
                continue
        return response 

    def run(self):
        self.logger.start_scraping_run()

        if self.config.get('hasCategories'):
            self.handle_with_categories(self.url)  
        else:
            if self.config.get('hasItems'):
                self.handle_with_items(self.url)       
            else:
                self.process_item({'url':self.url})
        self.logger.result_sent(self.result)
        self.logger.finished_scraping_run()

    def handle_with_categories(self, url):
     
        if self.config.get('theRootUrlIsACategory'):
            self.handle_with_items( url)
        for category in self.get_elements_to_process_from_webpage(url, self.config['selectorCategories']):
            url =  (  self.config.get('prefixToCategory')  if self.config.get('prefixToCategory') else '') + category.get('href')
            self.handle_with_items( url )

    def handle_with_items(self,url):
        if self.config.get('hasPagination'):
            urlToScrape = url
            while(urlToScrape):
                self.process_items(urlToScrape)
                urlToScrape = self.callbackGetNextLink(self.pageSoup.select_one(self.config['selectorPagination']))
        else:
            self.process_items(url)
    
    def process_items(self,url):
        for item in self.get_elements_to_process_from_webpage(url, self.config['selectorItems']):
            self.process_item(self.callbackBuildDataItem(item))

    def get_elements_to_process_from_webpage(self, url, selector ):
        response = requests.get(url)
        self.pageSoup = BeautifulSoup(response.content, 'html.parser')
        self.logger.looking_for_items_in_page(url)
        return self.pageSoup.select(selector)


    def process_item(self, data):
        
        if not data.get('content'):
            self.logger.scraping_item(data.get('url'))
            response = self.get_response( data.get('url') )
            item = BeautifulSoup(response.content,'html.parser')
        else:
            item = data['content']
    
        result = self.get_result(item, data, self.logger)
        self.result['items'].append(result)

        self.processor.send(result, self)
        self.logger.result_sent(result)

        if self.config.get('childrenSelector'):
            children =  self.callbackGetChildren( item.select( self.config.get('childrenSelector')))
            for childUrl in children:
                self.process_item( { 'url': childUrl})

    def get_result(self, item, data, logger):
        return self.callbackGetResult(item,data,logger) if self.callbackGetResult else  get_result_by_mapping(item,data,self.mapSelectorValue)


    

    





