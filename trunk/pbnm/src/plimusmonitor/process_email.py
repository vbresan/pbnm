#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import logging, email
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app

from plimusmonitor.classes.Credential import Credential

################################################################################
 
"""
"""
class MailProcessor(InboundMailHandler):
    
    sender  = 'vendors@plimus.com'
    subject = 'Your Plimus Account'
    
    username_tag = 'Username: '
    password_tag = 'Password: '
    
    """
    """
    def get_plimusId(self, subject):
        
        plimusId = ''
        
        beginTag = ': '
        endTag = ')'
        
        beginIndex = subject.find(beginTag)
        if beginIndex != -1:
            
            beginIndex += len(beginTag)
            endIndex = subject.find(endTag, beginIndex)
            if endIndex != -1:
                plimusId = subject[beginIndex : endIndex]
        
        return plimusId
    
    """
    """
    def save_credential(self, username, password, plimusId):
        
        if len(username) > 0 and len(password) > 0 and len(plimusId) > 0:
            
            credential = Credential.get(plimusId)
            credential.username = username
            credential.password = password
            credential.put()
    
    """
    """
    def receive(self, message):
        
        if message.sender == self.sender and message.subject.startswith(self.subject):
    
            bodies = message.bodies('text/plain')
            for contentType, body in bodies:
                
                username = ''
                password = ''
                plimusId = self.get_plimusId(message.subject)
                
                lines = body.decode().splitlines()
                for line in lines:
                    
                    if line.startswith(self.username_tag):
                        username = line.split()[-1]
                    elif line.startswith(self.password_tag):
                        password = line.split()[-1]
                
                self.save_credential(username, password, plimusId)

################################################################################

application = webapp.WSGIApplication([MailProcessor.mapping()], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main() 