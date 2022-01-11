from mongoengine import *
from datetime import datetime


class Keyword(EmbeddedDocument):
    id = IntField(required=True)
    AdsetId = IntField(required=True)
    name = StringField(required=True)
    text = StringField(required=True)
    createdAt = DateTimeField(default=datetime.utcnow)


class Ad(EmbeddedDocument):
    id = IntField(required=True)
    keywordId = IntField(required=True)
    image = StringField(required=True)
    name = StringField(required=True)
    headline1 = StringField(required=True)
    headline2 = StringField(required=True)
    createdAt = DateTimeField(default=datetime.utcnow)


class Adset(EmbeddedDocument):
    id = IntField(required=True)
    campaignId = IntField(required=True)
    name = StringField(required=True)
    avatar = StringField(required=True)
    tags = ListField()
    keywords = ListField(EmbeddedDocumentField(Keyword))
    ads = ListField(EmbeddedDocumentField(Ad))
    createdAt = DateTimeField(default=datetime.utcnow)
    updatedAt = DateTimeField(default=datetime.utcnow)


class Campaign(Document):
    meta = {
        "collection": "campaigns"
    }

    id = IntField(required=True, primary_key=True)
    name = StringField(required=True)
    avatar = StringField(required=True)
    dailyBudget = IntField(required=True, default=0)
    adsets = ListField(EmbeddedDocumentField(Adset))
    createdAt = DateTimeField(default=datetime.utcnow)
    updatedAt = DateTimeField(default=datetime.utcnow)


class Metadata(Document):
    id = IntField(required=True, primary_key=True)
    syncDownAt = DateTimeField()
    syncUpAt = DateTimeField()