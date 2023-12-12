from mongoengine import Document, StringField, ReferenceField, ListField

class Request(Document):
    title = StringField(required=True)
    support_type = ListField(StringField(), required=True) 
    description = StringField(required=True)
    user = ReferenceField('User', required=True)
    status = StringField(default='Pending')  # Add the status field with a default value
