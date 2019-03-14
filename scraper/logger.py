import logging
import sys
import traceback

class Logger:
    def __init__(self, scraper):
        self.logger = logger = logging.getLogger(__name__)
    def start_scraping_run(self, paginated=False):
        self.logger.info('START SCRAPING RUN')
        
    def scraping_item(self, url):
        self.logger.info('SCRAPING ITEM: %s', url)

    def result_sent(self, result):
        self.logger.info('RESULT SENT')

    def found_items_in_page(self, items, page_url):
        self.logger.info('FOUND %s ITEMS IN PAGE, url: %s',
                         len(items), page_url)

    def request_failed(self, url, response):
        self.logger.error('REQUEST FAILED:\nurl: %s\nstatus_code: %s', url,
                          response.status_code)

    def looking_for_items_in_page(self, url):
        self.logger.info('LOOKING FOR ITEMS IN PAGE: %s', url)

    def unexpected_termination(self):
        exception_info = ''.join(traceback.format_exception(*sys.exc_info()))
        self.logger.critical('UNEXPECTED TERMINATION:\n%s', exception_info)

    def finished_scraping_run(self):
        self.logger.info('FINISHED SCRAPING RUN')

    def custom(self, custom_message):
        self.logger.warning('CUSTOM: %s', custom_message)

