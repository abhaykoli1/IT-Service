from mongoengine import Document, StringField, BooleanField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentField
from pydantic import BaseModel
from typing import List

# MongoEngine EmbeddedDocument for features
class Feature(EmbeddedDocument):
    label = StringField(required=True)
    included = BooleanField(required=True)

# Main MongoEngine Document
class PricingPlan(Document):

    title = StringField(required=True)
    price = FloatField(required=True)
    monthly = BooleanField(required=True)
    description = StringField(required=True)
    discount = StringField()
    features = ListField(EmbeddedDocumentField(Feature))
    meta = {'collection': 'pricing_plans'}


# Pydantic Schemas
class FeatureSchema(BaseModel):
    label: str
    included: bool

class PricingPlanSchema(BaseModel):

    title: str
    price: float
    monthly: bool
    description: str
    discount: str
    features: List[FeatureSchema]

class PricingPlanResponse(PricingPlanSchema):
    id: str

    class Config:
        from_attributes = True  # for Pydantic v2+
