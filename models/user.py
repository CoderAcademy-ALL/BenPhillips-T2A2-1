from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = "users"

    # Define the columns of the "users" table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Define the relationship with Review model
    reviews = db.relationship('Review', back_populates='user')

    # Define the relationship with Comment model
    comments = db.relationship('Comment', back_populates='user')


class UserSchema(ma.Schema):
    # Define the serialization and deserialization schema for User model

    # Nested fields to include reviews and comments information within the user schema
    reviews = fields.List(fields.Nested('ReviewSchema'), exclude=['user', 'id'])
    comments = fields.List(fields.Nested('CommentSchema'))

    class Meta:
        # Specify the fields to be included in the serialized output
        fields = ('id', 'username', 'email', 'password', 'is_admin', 'reviews', 'comments')
