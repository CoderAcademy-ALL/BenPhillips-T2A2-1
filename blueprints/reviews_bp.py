from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
from models.user import User
from models.book import Book
from models.review import Review
from init import db
from blueprints.auth_bp import admin_or_owner_required

reviews_bp = Blueprint('reviews', __name__)

# Route to add a new review
@reviews_bp.route('/add_review', methods=['POST'])
@jwt_required()
def add_review():
    # Get review data from the request JSON
    review_data = request.json

    # Extract book ID from the data and retrieve the corresponding book
    book_id = review_data['book_id']
    book = Book.query.get(book_id)

    # Get user information from the JWT token
    user_email = get_jwt_identity()
    stmt = db.select(User).filter_by(email=user_email)
    user = db.session.scalar(stmt)

    # Create a new Review object
    new_review = Review(
        review_content=review_data['review_content'],
        date_created=date.today(),
        username=user.username,
        book_id=review_data['book_id'],
        user_id=user.id,
        title=book.title
    )

    # Associate the review with the user and book
    user.reviews.append(new_review)
    book.reviews.append(new_review)

    # Add the review to the session and commit changes
    db.session.add(new_review)
    db.session.commit()

    return jsonify(message='Review added successfully'), 201

# Route to update a review
@reviews_bp.route('/update_review', methods=['PUT'])
@jwt_required()
def update_review():
    # Get review ID from the request JSON
    review_id = int(request.json['review_id'])

    # Retrieve the review based on the provided review ID
    review = Review.query.filter_by(review_id=review_id).first()

    if review:
        # Check if the current user is an admin or the owner of the review
        admin_or_owner_required(review.user.email)
        
        # Update the review content
        review.review_content = request.json['review_content']
        
        # Commit the changes to the session
        db.session.commit()

        return jsonify(message="You updated a review!"), 202
    else:
        return jsonify(message="Review does not exist"), 404

# Route to delete a review
@reviews_bp.route('/delete_review/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id: int):
    # Retrieve the review based on the provided review ID
    review = Review.query.filter_by(review_id=review_id).first()

    if review:
        # Check if the current user is an admin or the owner of the review
        admin_or_owner_required(review.user.email)
        
        # Delete the review from the session and commit changes
        db.session.delete(review)
        db.session.commit()

        return jsonify(message="You deleted a review"), 202
    else: 
        return jsonify(message="That review does not exist"), 202
