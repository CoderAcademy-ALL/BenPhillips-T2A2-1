from init import db, ma
from marshmallow import fields


class Comment(db.Model):
    __tablename__ = "comments"

    # Define the columns of the "comments" table
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date())

    # Define the foreign key and relationship with the User model
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    username = db.Column(db.String, nullable=False)
    user = db.relationship('User', back_populates='comments')

    # Define the foreign key and relationship with the Review model
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.review_id', ondelete='CASCADE'), nullable=False)
    review = db.relationship('Review', back_populates='comments')

class CommentSchema(ma.Schema):
    # Define the serialization and deserialization schema for Comment model

    # Nested fields to include user and review information within the comment schema
    user = fields.Nested('UserSchema', only=['username'])
    review = fields.Nested('ReviewSchema', only=['review_id'])

    class Meta:
        # Specify the fields to be included in the serialized output
        fields = ('comment_content', 'username', 'comment_id', 'review', 'review_id')
        ordered = True
