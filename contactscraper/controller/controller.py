#scrapy
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider

#Local imports
from contactscraper.spiders.contactspider import ContactSpider

#std packages
import re
import logging
import os
from os import path
from datetime import datetime, timezone, timedelta
import sys

#Twisted
from twisted.internet import reactor, defer

#tld
import tldextract

class Controller:
    def __init__(self, starting_urls, scrape_numbers=True, scrape_emails=True, region="US", max_results=False, website_name='output.json'):

        
        #Init logging
        start_time = datetime.now().timestamp()
        logging.basicConfig(filename=path.join('logs',f'{start_time}.log'),level=logging.INFO)
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

        #Init project with scrapy settings
        self.settings = Settings()
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'contactscraper.settings'
        settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
        self.settings.setmodule(settings_module_path, priority='project')

        #Init instance variables
        self.starting_urls = starting_urls
        self.scrape_numbers = scrape_numbers
        self.scrape_emails = scrape_emails
        self.region = region
        self.max_results = max_results
        self.website_name = website_name
    
        logging.info(f"Scrapping for {starting_urls}")
        

    def scrape(self):
        '''
        * * * * *
        * Linearly spins up instances of ContactSpider for each url in starting_urls
        * This function ensures atomicity between ContactSpiders by spinning up a Twisted Reactor and using deferred callbacks.
        *
        * see: https://twistedmatrix.com/documents/current/api/twisted.internet.reactor.html
        * and: https://twistedmatrix.com/documents/current/api/twisted.internet.defer.inlineCallbacks.html
        * * * * *
        * @param self : current instance of Controller
        * @return void
        * * * * *
        '''
        
        runner = CrawlerRunner(self.settings)
        configure_logging()
        logging.getLogger('scrapy').propagate = False



        @defer.inlineCallbacks
        def crawl(starting_urls, website_name):
            for starting_url in starting_urls:
                ext = tldextract.extract(starting_url)
                # logging.info(ext)
                root = '.'.join(ext[1:])
                # logging.info(root)
                # break
                try:
                    
                    yield runner.crawl(ContactSpider, 
                                        root=root, 
                                        region=self.region,
                                        scrape_emails=self.scrape_emails,
                                        scrape_numbers=self.scrape_numbers,
                                        start_urls=[starting_url], 
                                        allowed_domains=[root],
                                        max_results=self.max_results,
                                        website_name=website_name
                                        )                   
                except Exception as e:
                    logging.warning(f"FATAL: NEW MAIL-SPIDER FAILED TO LAUNCH\n\t{str(e)}")
            reactor.stop()
        
        
        crawl(self.starting_urls, self.website_name)

        reactor.run() 
