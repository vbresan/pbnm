#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import urllib
import logging

from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from plimusmonitor.classes.Credential import Credential
from plimusmonitor.classes.CustomHTMLParser import CustomHTMLParser

################################################################################

"""
"""
class Scraper(webapp.RequestHandler):
    
    """
    """
    def strip_page(self, page):
        
        beginIndex = page.find('<td align=center class="bold10MaroonOnGray" nowrap>Affiliate</td>')
        if beginIndex != -1:
            
            beginIndex = page.find('</tr>', beginIndex)
            if beginIndex != -1:
            
                endIndex = page.find('</table><br>', beginIndex)
                if endIndex != -1:
                    return page[beginIndex : endIndex]
    
        return ''
    
    """
    """
    def reverse_rows(self, page):
        
        reversed = ''
        
        beginIndex = page.find('<tr>')
        while beginIndex != -1:
            
            endIndex = page.find('</tr>', beginIndex)
            if endIndex != -1:
                
                endIndex += len('</tr>')
                reversed = page[beginIndex : endIndex] + reversed
            
                beginIndex = page.find('<tr>', endIndex)
            else:
                break
            
        return reversed
    
    """
    """
    def get_url(self, identifier):
        
        url = 'https://secure.plimus.com/jsp/developer_monitor.jsp?sessionId='
        
        credentials = Credential.gql("WHERE identifier = :1", identifier)
        if credentials.count() > 0:
            if credentials[0].sessionId != None:
                url += credentials[0].sessionId
        
        return url
    
    """
    """
    def scrape_page(self, page, identifier):
        
        page = self.strip_page(page)
        page = self.reverse_rows(page)
        
        if len(page) != 0:
            
            htmlParser = CustomHTMLParser(identifier)
            htmlParser.feed(page)
            htmlParser.close()
        
    """
    """
    def post(self):
        
        identifier = self.request.get("identifier")
        if len(identifier) > 0:
            
            url = self.get_url(identifier)
            logging.info('Scraping URL: ' + url)
            
            handle = urllib.urlopen(url)
            if handle.geturl() == url:
                
                page = handle.read()
                self.scrape_page(page, identifier)
                
                logging.info('Done!')
            else:
                taskqueue.Queue("login").add(taskqueue.Task(
                    url    = "/plimusmonitor/login", 
                    params = {"identifier": identifier}
                ))
        
    """
    """
    def get(self):
        self.post()

################################################################################

application = webapp.WSGIApplication(
     [("/plimusmonitor/scrape", Scraper)],
     debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
