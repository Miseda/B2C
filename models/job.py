from mongoengine import Document, StringField, EmailField
from flask_login import UserMixin

class Job(Document,UserMixin):
    title = StringField(required=True)
    location = StringField(required=True)
    type = StringField(required=True, choices=['On-Site', 'Hybrid', 'Remote'])
    description = StringField(required=True)