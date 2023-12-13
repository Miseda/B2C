# models/contact_report.py
from mongoengine import Document, StringField

class ContactReport(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message = StringField(required=True)
