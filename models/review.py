from init import db, ma
from marshmallow import fields

class Review(db.Model):
    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, primary_key=True)
    review_content = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    username = db.Column(db.String, nullable=False)
    user = db.relationship('User', back_populates='reviews')

    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String, nullable=False)
    book = db.relationship('Book', back_populates='reviews')

    comments = db.relationship('Comment', back_populates='review', cascade='all, delete')



class ReviewSchema(ma.Schema):
  user = fields.Nested('UserSchema', exclude=['reviews', 'username'])
  book = fields.Nested('BookSchema')
  comments = fields.List(fields.Nested('CommentSchema', exclude=['review', 'review_id']))

  class Meta:
    fields = ('review_id', 'review_content', 'date_created', 'id', 'username', 'comments', 'title')
    ordered = True