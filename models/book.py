from init import db, ma
from marshmallow import fields

class Book(db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False, unique=True)
    genre = db.Column(db.String, nullable=False)
    synopsis = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

    reviews = db.relationship('Review', back_populates='book', cascade='all, delete')

class BookSchema(ma.Schema):
    reviews = fields.List(fields.Nested('ReviewSchema', only=['username', 'review_content', 'review_id', 'date_created', 'comments']))
    
    class Meta:
        fields = ('book_id', 'title', 'author', 'genre', 'synopsis', 'publication_year', 'user', 'reviews')