from google.appengine.ext import db

"""
"""
class Entry(db.Model):
    
    formKey = db.StringProperty()
    email   = db.StringProperty()
    name    = db.StringProperty()
    product = db.StringProperty()
