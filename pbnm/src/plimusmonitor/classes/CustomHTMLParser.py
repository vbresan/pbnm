import hashlib
import logging
import string
import re

from datetime import datetime
from HTMLParser import HTMLParser

from FeedItem import FeedItem


"""
"""
class CustomHTMLParser(HTMLParser):
    
    nextDataNameIndex = 0
    dataNames = [
      'Time', 
      'Action', 
      'Account', 
      'IP Address', 
      'Product',
      'Curr',
      'From Computer',
      'Affiliate'
    ]
    
    """
    """
    def resetItemData(self):
        
        self.isItemOpened    = False
        self.isLinkOpened    = False
        self.isItemTitle     = False
        self.itemTitle       = ''
        self.itemHash        = ''
        self.itemDescription = '<table>'
        self.capturedData    = ''
        
    """
    """
    def isItemStart(self, tag):
        return tag.lower() == 'tr' and not self.isItemOpened
    
    """
    """
    def isItemEnd(self, tag):
        return tag.lower() == 'tr' and self.isItemOpened
    
    """
    """
    def isDataTag(self, tag):
        return tag.lower() == 'td' and self.isItemOpened
    
    """
    """
    def isLinkTag(self, tag):
        return tag.lower() == 'a' and self.isItemOpened
       
    """
    """
    def appendDataName(self):
        
        currentDataNameIndex = self.nextDataNameIndex % len(self.dataNames)
        currentDataName = self.dataNames[currentDataNameIndex]
        
        self.itemDescription += '<tr><td>' + currentDataName + ':</td><td>' 
        
        if currentDataName == 'Action' or currentDataName == 'Product':
            self.isItemTitle = True
        else:
            self.isItemTitle = False
        
        self.nextDataNameIndex += 1
        
    """
    """
    def appendLinkStartTag(self, tag, attrs):
        
        target = attrs.get('target', '')
        
        self.itemDescription += '<a href="' + attrs['href'] + '" target="' + target + '">'
        self.isLinkOpened = True
        
    """
    """
    def appendLinkEndTag(self):
        self.itemDescription += '</a>'
        self.isLinkOpened = False
    
    """
    """
    def isItemNew(self):
        
        feedItems = FeedItem.gql(
             "WHERE hash = :1 AND identifier = :2", 
             self.itemHash, 
             self.identifier
        )
        
        if feedItems.count() == 0: 
            return True
       
        return False
   
    """
    """
    def saveItem(self):
        
        if self.isItemNew() == True:
            
            feedItem = FeedItem()
            
            feedItem.title       = self.itemTitle.strip().decode('utf-8')
            feedItem.link        = self.itemLink
            feedItem.hash        = self.itemHash
            feedItem.description = self.itemDescription.decode('utf-8')
            feedItem.identifier  = self.identifier
            
            feedItem.put()
            logging.info('Saving item: ' + feedItem.title)
               
    """
    """
    def __init__(self, identifier):
        HTMLParser.__init__(self)

        self.currentPath = ''
        
        self.itemLink = 'https://secure.plimus.com/jsp/developer_login.jsp'
        self.identifier = identifier
        
        self.resetItemData()
        
        logging.info('Parsing page.')

    """
    """
    def handle_starttag(self, tag, attrs):
        
        attrs = dict(attrs)
        
        if self.isItemStart(tag):
            self.isItemOpened = True
        elif self.isDataTag(tag):
            self.appendDataName()
        elif self.isLinkTag(tag):
            self.appendLinkStartTag(tag, attrs)
        
        self.currentPath += '/' + tag
        
    """
    """
    def handle_entityref(self, entity):
        
        if entity == 'nbsp':
            if self.isItemTitle:
                self.itemTitle = self.itemTitle.rstrip() + '&nbsp;'

            self.capturedData = self.capturedData.rstrip() + '&nbsp;'

    """
    """
    def handle_data(self, data):
        
        data = data.strip()
        self.capturedData += data
            
        
    """
    """
    def handle_endtag(self, tag):

        self.currentPath = string.rsplit(self.currentPath, '/', 1)[0]
        
        if self.isDataTag(tag):
            
            if self.isItemTitle:
                if len(self.itemTitle) == 0:
                    self.itemTitle = self.capturedData
                else:
                    self.itemTitle += ' (' + self.capturedData + ')'
                
            self.itemDescription += self.capturedData
            self.capturedData = ''
            
            if self.isLinkOpened:
                self.appendLinkEndTag()
            
            self.itemDescription += '</td></tr>' 
            
            self.itemHash = hashlib.sha1(self.itemDescription).hexdigest()
            
        if self.isItemEnd(tag):
            self.itemDescription += '</table>'
            self.saveItem()
            self.resetItemData()
