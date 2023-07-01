from init import db, ma
from marshmallow import fields


class Review(db.Model):
    __tablename__ = "reviews"

    # Define the columns of the "reviews" table
    review_id = db.Column(db.Integer, primary_key=True)
    review_content = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date())

    # Define the foreign key and relationship with the User model
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    username = db.Column(db.String, nullable=False)
    user = db.relationship('User', back_populates='reviews')

    # Define the foreign key and relationship with the Book model
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String, nullable=False)
    book = db.relationship('Book', back_populates='reviews')

    # Define the relationship with Comment model
    comments = db.relationship('Comment', back_populates='review', cascade='all, delete')


class ReviewSchema(ma.Schema):
    # Define the serialization and deserialization schema for Review model

    # Nested fields to include user, book, and comments information within the review schema
    user = fields.Nested('UserSchema', exclude=['reviews', 'username'])
    book = fields.Nested('BookSchema')
    comments = fields.List(fields.Nested('CommentSchema', exclude=['review', 'review_id']))

    class Meta:
        # Specify the fields to be included in the serialized output
        fields = ('review_id', 'review_content', 'date_created', 'id', 'username', 'comments', 'title')
        ordered = True
