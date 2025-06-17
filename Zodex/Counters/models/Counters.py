from mongoengine import Document, StringField, IntField
from pydantic import BaseModel

class CountersTable(Document):
    build= StringField(required =True)
    identity = StringField(required =True)
    growth = StringField(required =True)
   
    

class CountersModel(BaseModel):
    build :str
    identity :str
    growth :str
