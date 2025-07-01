from mongoengine import Document, StringField, ListField, URLField
from pydantic import BaseModel, HttpUrl
from typing import List

# MongoEngine Model
class TechCard(Document):
    image = StringField(required=True)  # Image path or URL
    title = StringField(required=True)
    techStack = ListField(StringField(), required=True)
    link = StringField(required=True)
    meta = {'collection': 'techcards'}

# Pydantic Schemas
class TechCardSchema(BaseModel):
    image: str
    techStack: List[str]
    title: str
    link: str

