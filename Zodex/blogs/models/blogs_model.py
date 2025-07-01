from mongoengine import Document, StringField, DateTimeField, ReferenceField
from pydantic import BaseModel
from datetime import datetime

from Zodex.blog_category.models.blog_category_model import CategoryTable

# MongoEngine Model
class BlogTable(Document):
    seo_title = StringField(required=True)
    seo_desc = StringField(required=True)
    image = StringField(required=True)
    title = StringField(required=True)
    author = StringField(required=True)
    short_desc = StringField(required=True)
    desc = StringField(required=True)
    tag = StringField(required=True)
    category = ReferenceField(CategoryTable, required=True)  
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        if not self.created_at:
            self.created_at = datetime.utcnow()
        return super(BlogTable, self).save(*args, **kwargs)

# Pydantic Schema
class BlogModel(BaseModel):
    image: str
    seo_title: str
    seo_desc: str
    title: str
    author: str
    short_desc: str
    desc: str
    tag: str
    category: str  # ID of the category
