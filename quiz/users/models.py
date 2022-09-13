from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import Document, IntField,StringField,EmailField,ReferenceField

class User(Document):
    username = StringField(required=True)
    fullname = StringField(required=True)
    email = EmailField(required=True,unique=True)
    password = StringField()


    def set_password(self, password):
         self.password = generate_password_hash(password)
         self.save()

    def check_password(self,password):
        return check_password_hash(self.password,password)

