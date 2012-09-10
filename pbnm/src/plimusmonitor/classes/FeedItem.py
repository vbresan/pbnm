from google.appengine.ext import db

"""
"""
class FeedItem(db.Model):
    
    title       = db.StringProperty()
    link        = db.StringProperty()
    hash        = db.StringProperty()
    description = db.TextProperty()
    pubDate     = db.DateTimeProperty(auto_now_add=True)
    identifier  = db.StringProperty()
