from google.appengine.ext import db

"""
"""
class KeyPair(db.Model):
    
    identifier = db.StringProperty()
    formKey    = db.StringProperty()
    
    @staticmethod
    def get(plimusId):
        
        credentials = Credential.gql("WHERE plimusId = :1", plimusId)
        if credentials.count() != 0:
            return credentials[0]
        else:
            credential = Credential()
            credential.plimusId = plimusId
            
            return credential
    
    @staticmethod
    def get_with_identifier(identifier):
        
        credentials = Credential.gql("WHERE identifier = :1", identifier)
        if credentials.count() > 0:
            return credentials[0]
        else:
            return None
