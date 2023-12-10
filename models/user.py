from mongoengine import Document, StringField, EmailField
from flask_login import UserMixin


class User(Document, UserMixin):
    full_name = StringField(required=True)
    phone_number = StringField(required=True)  # You might want to use a specialized field for phone numbers
    email = EmailField(unique=True, required=True)
    password = StringField(required=True)
    role = StringField(default='User')
    
    # Add the reset_token field
    reset_token = StringField()
    
class Job(Document,UserMixin):
    title = StringField(required=True)
    location = StringField(required=True)
    type = StringField(required=True, choices=['Site', 'Hybrid', 'Remote'])
    description = StringField(required=True)
