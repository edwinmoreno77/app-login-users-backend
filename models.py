from mongoengine import connect, Document, StringField, EmailField, BooleanField, DateTimeField, DictField
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config

# Conectar a MongoDB Atlas
connect(host=Config.MONGODB_SETTINGS['host'])

class User(Document):
    name = StringField(required=True, max_length=100)
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    last_login = DateTimeField()
    profile = DictField(default={
        'avatar': None,
        'phone': None,
        'address': None
    })

    meta = {
        'collection': 'users',
        'indexes': [
            'email',
            'is_active',
            'created_at'
        ],
        'ordering': ['-created_at']
    }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.updated_at = datetime.utcnow()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        self.last_login = datetime.utcnow()
        self.save()

    @classmethod
    def get_by_email(cls, email):
        return cls.objects(email=email).first()

    @classmethod
    def get_by_id(cls, user_id):
        return cls.objects(id=user_id).first()

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z') if self.updated_at else None,
            'last_login': self.last_login.strftime('%Y-%m-%dT%H:%M:%S.%f%z') if self.last_login else None,
            'profile': self.profile
        }

    def to_public_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'email': self.email,
            'profile': self.profile
        }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f"User: {self.email}"


