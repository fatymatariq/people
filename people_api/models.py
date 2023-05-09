from people_api.config import db, ma
from datetime import datetime
from marshmallow_sqlalchemy import fields
from flask import current_app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import URLSafeTimedSerializer as Serializer, BadSignature, SignatureExpired


class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32), unique=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default = datetime.utcnow, onupdate=datetime.utcnow
    )

    notes = db.relationship(
        Note,
        backref="person",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Note.timestamp)"
    )


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
    
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
    
    def generate_auth_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expiration)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user       

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = True
        sqla_session = db.session
        include_fk = True


class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True
        sqla_session = db.session
        include_relationships = True
    
    notes = fields.Nested(NoteSchema, many=True)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        exclude = ['password_hash']


person_schema = PersonSchema()
people_schema = PersonSchema(many=True)
note_schema = NoteSchema()
user_schema = UserSchema()