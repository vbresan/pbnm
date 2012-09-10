#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

from google.appengine.api import taskqueue
from email_extractor.classes.KeyPair import KeyPair

################################################################################

#TODO: check for result size limitation!!!
keyPairs = KeyPair.gql("WHERE identifier != :1", None)
for keyPair in keyPairs:
    
    taskqueue.Queue("extract").add(taskqueue.Task(
        url    = "/email_extractor/extract", 
        params = {
          "identifier": keyPair.identifier, 
          "formKey": keyPair.formKey
        }
    ))

