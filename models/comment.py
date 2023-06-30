from init import db, ma
from marshmallow import fields


class Comment(db.Model):
    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    username = db.Column(db.String, nullable=False)
    user = db.relationship('User', back_populates='comments')

    review_id = db.Column(db.Integer, db.ForeignKey('reviews.review_id', ondelete='CASCADE'), nullable=False)
    review = db.relationship('Review', back_populates='comments')

class CommentSchema(ma.Schema):
  user = fields.Nested('UserSchema', only=['username'])
  review = fields.Nested('ReviewSchema', only=['review_id'])

  class Meta:
    fields = ('comment_content', 'username', 'review', 'review_id')
    ordered = True