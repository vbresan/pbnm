#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################################################

from google.appengine.api import taskqueue
from plimusmonitor.classes.Credential import Credential

################################################################################

#TODO: check for result size limitation!!!
credentials = Credential.gql("WHERE identifier != :1", None)
for credential in credentials:
    
    taskqueue.Queue("scrape").add(taskqueue.Task(
        url="/plimusmonitor/scrape", 
        params={"identifier": credential.identifier}
    ))
