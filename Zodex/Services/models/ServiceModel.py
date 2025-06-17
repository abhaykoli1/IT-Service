from mongoengine import Document,StringField,IntField
from pydantic import BaseModel

class ServiceTable(Document):
    icon = StringField(required = True)
    title = StringField(required =True)
    description = StringField(required =True)

class ServiceModel(BaseModel):
    icon : str 
    title : str 
    description : str 

