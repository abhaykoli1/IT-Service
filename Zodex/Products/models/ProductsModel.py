from mongoengine import Document, StringField, IntField
from pydantic import BaseModel

class ProductTable(Document):
    image = StringField(required = True)
    title = StringField(required =True)
    type = StringField(required =True)

class ProductModel(BaseModel):
    image : str
    title : str
    type : str