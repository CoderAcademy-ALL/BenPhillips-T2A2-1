from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
from models.user import User
from models.comment import Comment
from init import db
from blueprints.auth_bp import admin_or_owner_required

comments_bp = Blueprint('comments', __name__)

# Route to create a new comment
@comments_bp.route("/add_comment", methods=["POST"])
@jwt_required()
def create_comment():
    # Get comment data from the request JSON
    comment_data = request.json

    # Extract comment content and review ID from the data
    comment_content = comment_data.get('comment_content')
    review_id = comment_data.get('review_id')

    # Get user information from the JWT token
    user_email = get_jwt_identity()
    stmt = db.select(User).filter_by(email=user_email)
    user = db.session.scalar(stmt)

    # Create a new Comment object
    new_comment = Comment(
        comment_content=comment_content,
        username=user.username,
        user_id=user.id,
        review_id=review_id,
        date_created=date.today()
    )

    # Add the comment to the session and commit changes
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({'message': 'Comment created successfully'})

# Route to delete a comment
@comments_bp.route("/delete_comment/<comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id):
    # Fetch the comment based on the provided comment ID
    comment = Comment.query.get(comment_id)

    if comment:
        # Check if the current user is an admin or the owner of the comment
        admin_or_owner_required(comment.user.email)
        
        # Delete the comment from the session and commit changes
        db.session.delete(comment)
        db.session.commit()

        return jsonify({'message': 'Comment deleted successfully'})
    else:
        return jsonify({'message': 'Comment not found'})

# Route to edit a comment
@comments_bp.route("/edit_comment/<comment_id>", methods=["PUT"])
@jwt_required()
def edit_comment(comment_id):
    # Fetch the comment based on the provided comment ID
    comment = Comment.query.get(comment_id)

    if comment:
        # Check if the current user is an admin or the owner of the comment
        admin_or_owner_required(comment.user.email)
        
        # Get updated comment data from the request JSON
        data = request.get_json()
        
        # Update the comment content
        comment.comment_content = data.get('comment_content')

        # Commit the changes to the session
        db.session.commit()

        return jsonify({'message': 'Comment updated successfully'})
    else:
        return jsonify({'message': 'Comment not found'})
