#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import logging, email
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app

################################################################################
 
"""
"""
class MailProcessor(InboundMailHandler):
    
    """
    """
    def receive(self, message):
        
        logging.info('From: ' + message.sender)
        logging.info('Subject: ' + message.subject)
    
        bodies = message.bodies('text/plain')
        for contentType, body in bodies:
            logging.info('Body: ' + body.decode())

################################################################################

application = webapp.WSGIApplication([MailProcessor.mapping()], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main() 