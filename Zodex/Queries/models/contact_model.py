from mongoengine import Document, StringField, DateTimeField
from pydantic import BaseModel, Field
from datetime import datetime

class ContactQueryTable(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    phone = StringField(required=True)
    code = StringField(required=True)
    email = StringField(required=True)
    message = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.utcnow()
        return super(ContactQueryTable, self).save(*args, **kwargs)

class ContactQueryModel(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    phone: str = Field(...)
    email: str = Field(...)
    code: str = Field(...)
    message: str = Field(...)
