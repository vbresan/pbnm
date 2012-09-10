#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

import logging
import urllib

from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from plimusmonitor.classes.Credential import Credential

################################################################################

"""
"""
class Login(webapp.RequestHandler):
    
    url = 'https://secure.plimus.com/jsp/developer_login.jsp'
    
    """
    """
    def get_sessionId(self):
        
        sessionId = ''
        
        page = urllib.urlopen(self.url).read()
        
        begin_tag = "<input type=hidden name=sessionId value='"
        end_tag   = "'>"
        
        begin_index = page.find(begin_tag)
        if begin_index != -1:
            
            begin_index += len(begin_tag)
            
            end_index = page.find(end_tag, begin_index)
            if end_index != -1:
                sessionId = page[begin_index : end_index] 
        
        return sessionId
    
    """
    """
    def get_parameters(self, credential, sessionId):
        
        params = urllib.urlencode({
           'username'    : credential.username,
           'password'    : credential.password,
           'sessionId'   : sessionId,
           'loginAction' : 'update'
        })
        
        return params

    """
    """
    def get_sessionId_from_url(self, url):
        
        sessionId = ''
        
        begin_tag = 'sessionId='
        
        begin_index = url.find(begin_tag)
        if begin_index != -1:
            
            begin_index += len(begin_tag)
            sessionId = url[begin_index : ]
        
        return sessionId
        
    
    """
    """
    def post(self):
    
        identifier = self.request.get("identifier")
        if len(identifier) > 0:
            
            credential = Credential.get_with_identifier(identifier) 
            if credential != None:
            
                sessionId = self.get_sessionId()
                if len(sessionId) > 0:
                    
                    params = self.get_parameters(credential, sessionId)
                    handle = urllib.urlopen(self.url, params)
                    
                    url = handle.geturl()
                    
                    sessionId = self.get_sessionId_from_url(url)
                    if len(sessionId) > 0:
                        
                        credential.sessionId = sessionId
                        credential.put()
                    
                        taskqueue.Queue("scrape").add(taskqueue.Task(
                            url    = "/plimusmonitor/scrape", 
                            params = {"identifier": identifier}
                        ))
        
    """
    """
    def get(self):
        self.post()

################################################################################

application = webapp.WSGIApplication(
     [("/plimusmonitor/login", Login)],
     debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
