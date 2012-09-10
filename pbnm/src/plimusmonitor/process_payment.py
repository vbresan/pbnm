#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import uuid

from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from plimusmonitor.classes.Credential import Credential

################################################################################

"""
"""
class PaymentProcessor(webapp.RequestHandler):
    
    """
    """
    def post(self):
        
        identifier = str(uuid.uuid4())
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(identifier)        
        
        plimusId = self.request.get('plimusId')
        if len(plimusId) > 0:
            
            credential = Credential.get(plimusId)
            credential.identifier = identifier
            credential.put()
            
            taskqueue.Queue("scrape").add(taskqueue.Task(
                url="/plimusmonitor/scrape", 
                params={"identifier": identifier}
            ))
        
    """
    """
    def get(self):
        self.post()

################################################################################

application = webapp.WSGIApplication(
     [('/process_payment', PaymentProcessor)],
     debug=True
)

def main(no_caching):
    run_wsgi_app(application)

if __name__ == "__main__":
    no_caching = True # can be anything, it's a dummy value
    main(no_caching)
