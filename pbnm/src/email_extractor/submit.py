#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import urllib

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from email_extractor.classes.Entry import Entry

################################################################################

"""
"""
class FormSubmitter(webapp.RequestHandler):
    
    """
    """
    def get_params(self, email, name, product):
        
        return urllib.urlencode({
           "entry.0.single": email, 
           "entry.1.single": name.encode("utf-8"), 
           "entry.2.single": product,
           "pageNumber": "0",
           "backupCache": "",
           "submit": "Envoyer"
        })
        
    """
    """
    def get_url(self, formKey):
        
        return "https://spreadsheets.google.com/formResponse?formkey=" + formKey + "&amp;ifq"
    
    """
    """
    def is_entry_new(self, formKey, email, name, product):
        
        entries = Entry.gql(
             "WHERE formKey = :1 AND email = :2 AND name = :3 AND product = :4", 
             formKey, email, name, product
        )
        
        if entries.count() == 0: 
            return True
       
        return False
    
    """
    """
    def post(self):
        
        formKey = self.request.get("formKey")
        email   = self.request.get("email")
        name    = self.request.get("name")
        product = self.request.get("product")
        
        if len(formKey) > 0 and len(email) > 0:
            
            if self.is_entry_new(formKey, email, name, product):
                
                params = self.get_params(email, name, product)
                url    = self.get_url(formKey)
                
                f = urllib.urlopen(url, params)
                f.read()
                
                # TODO: purge after some time
                # TODO: has bug as multiple tasks are commiting the same data
                entry = Entry()
                entry.formKey = formKey
                entry.email   = email
                entry.name    = name
                entry.product = product
                
                entry.put()
        
    """
    """
    def get(self):
        self.post()

################################################################################

application = webapp.WSGIApplication(
     [("/email_extractor/submit", FormSubmitter)],
     debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
