from mongoengine import Document, StringField
from pydantic import BaseModel

# MongoEngine Model
class CategoryTable(Document):
    name = StringField(required=True, unique=True)

    meta = {'collection': 'categories'}

# Pydantic Schema
class CategoryModel(BaseModel):
    name: str