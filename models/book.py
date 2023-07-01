from init import db, ma
from marshmallow import fields

class Book(db.Model):
    __tablename__ = "books"

    # Define the columns of the "books" table
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False, unique=True)
    genre = db.Column(db.String, nullable=False)
    synopsis = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

    # Define the relationship between Book and Review models
    reviews = db.relationship('Review', back_populates='book', cascade='all, delete')

class BookSchema(ma.Schema):
    # Define the serialization and deserialization schema for Book model

    # Nested field to include reviews within the book schema
    reviews = fields.List(fields.Nested('ReviewSchema', only=['username', 'review_content', 'review_id', 'date_created', 'comments']))
    
    class Meta:
        # Specify the fields to be included in the serialized output
        fields = ('book_id', 'title', 'author', 'genre', 'synopsis', 'publication_year', 'user', 'reviews')
