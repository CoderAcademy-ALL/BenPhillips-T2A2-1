from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    reviews = db.relationship('Review', back_populates='user')

    comments = db.relationship('Comment', back_populates='user')


class UserSchema(ma.Schema):
    reviews = fields.List(fields.Nested('ReviewSchema'), exclude=['user', 'id'])
    comments = fields.List(fields.Nested('CommentSchema'))

    class Meta:
        fields = ('id', 'username', 'email', 'password', 'is_admin', 'reviews', 'comments')