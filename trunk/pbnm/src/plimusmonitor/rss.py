#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import PyRSS2Gen

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from plimusmonitor.classes.FeedItem import FeedItem

################################################################################

"""
"""
class CustomRSSFeed(webapp.RequestHandler):
    
    rss = PyRSS2Gen.RSS2(
        title = 'Plimus.com - BuyNow Monitor',
        link  = 'http://www.plimus.com/',
        description = 'Recent BuyNow activities',
        generator = 'http://www.binarysolutions.biz/',
        docs = ''
      )
    
    """
    """
    def post(self, identifier):
        
        if len(identifier) > 0:
            
            items = FeedItem.gql(
                 "WHERE identifier = :1 ORDER BY pubDate DESC LIMIT 50",
                 identifier
            )
            
            for item in items:
                self.rss.items.append(PyRSS2Gen.RSSItem(
                                                            
                        title       = item.title, 
                        link        = item.link,
                        # description = '<![CDATA[' + item.description + ']]>',
                        description = item.description,
                        pubDate     = item.pubDate
                    ))
        
        self.response.headers['Content-Type'] = 'application/rss+xml'
        self.rss.write_xml(self.response.out, 'utf-8')
        
    
    """
    """
    def get(self, identifier):
        self.post(identifier)
    
################################################################################

application = webapp.WSGIApplication(
     [(r'/rss/(.*)', CustomRSSFeed)],
     debug=True
)

def main(no_caching):
    run_wsgi_app(application)

if __name__ == "__main__":
    no_caching = True # can be anything, it's a dummy value
    main(no_caching)
