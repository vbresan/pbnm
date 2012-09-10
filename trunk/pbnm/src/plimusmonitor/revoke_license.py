#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from plimusmonitor.classes.Credential import Credential

################################################################################

"""
"""
class LicenseRevoker(webapp.RequestHandler):
    
    """
    """
    def post(self):
        
        identifier = self.request.get('identifier')
        if len(identifier) > 0:
            
            credential = Credential.get_with_identifier(identifier) 
            if credential != None:
                
                #TODO: delete old feed items
                credential.identifier = None
                credential.put()
                    
    """
    """
    def get(self):
        self.post()

################################################################################

application = webapp.WSGIApplication(
     [('/revoke_license', LicenseRevoker)],
     debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
