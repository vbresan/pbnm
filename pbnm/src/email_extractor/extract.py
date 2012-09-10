#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import logging
import re
import urllib
import xml.dom.minidom

from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

################################################################################

"""
"""
class EmailExtractor(webapp.RequestHandler):

    """
    """
    def get_url(self, identifier):
        return "http://monitor.binarysolutions.biz/rss/" + identifier
    
    """
    """
    def get_items(self, identifier):
        
        url     = self.get_url(identifier)
        content = urllib.urlopen(url)
        doc     = xml.dom.minidom.parse(content)
        
        return doc.getElementsByTagName("item")
    
    """
    """
    def get_description(self, item):
        return item.getElementsByTagName("description")[0].firstChild.data
    
    """
    """
    def get_account(self, description):
        
        email = ""
        name  = ""
        
        m = re.search('<tr><td>Account:</td><td><a href="mailto:([^"]*)" target="">([^<]*)</a></td></tr>', description)
        if m != None:
            email = m.group(1)
            name  = m.group(2)
                
        return (email, name)
    
    """
    """
    def get_product(self, description):
        
        product = ""
        
        m = re.search('<tr><td>Product:</td><td>([^<]*)</td></tr>', description)
        if m != None:
            product = m.group(1)
                
        return product
    
    """
    """
    def post(self):
        
        identifier = self.request.get("identifier")
        formKey    = self.request.get("formKey")
        
        if len(identifier) > 0 and len(formKey) > 0:
            
            #TODO: optimize this
            items = self.get_items(identifier)
            for item in items:
                
                description = self.get_description(item)
                
                (email, name) = self.get_account(description)
                if email.find("@") != -1:
                    product = self.get_product(description)
                    
                    taskqueue.Queue("submit").add(taskqueue.Task(
                        url    = "/email_extractor/submit", 
                        params = {
                          "formKey": formKey,
                          "email": email,
                          "name": name,
                          "product": product
                        }
                    ))
                
        
    """
    """
    def get(self):
        self.post()

################################################################################

application = webapp.WSGIApplication(
     [("/email_extractor/extract", EmailExtractor)],
     debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
