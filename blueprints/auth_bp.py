from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import create_access_token, get_jwt_identity
from datetime import timedelta

from models.user import User, UserSchema

from init import db, bcrypt

auth_bp = Blueprint('auth', __name__)

# Function to check if the current user is an admin
def admin_required():
    # Get the email of the current user from the JWT token
    user_email = get_jwt_identity()
    # Fetch the user from the database based on the email
    stmt = db.select(User).filter_by(email=user_email)
    user = db.session.scalar(stmt)
    # Check if the user exists and is an admin
    if not (user and user.is_admin):
        abort(401, description='You must be an admin')

# Function to check if the current user is an admin or the owner of a resource
def admin_or_owner_required(owner_email):
    # Get the email of the current user from the JWT token
    user_email = get_jwt_identity()
    # Fetch the user from the database based on the email
    stmt = db.select(User).filter_by(email=user_email)
    user = db.session.scalar(stmt)
    # Check if the user exists and is an admin or the owner
    if not (user and (user.is_admin or user_email == owner_email)):
        abort(401, description='You must be an admin or the owner')

# Route to register a new user
@auth_bp.route("/register", methods=['POST'])
def register():
    # Get the form data
    email = request.form['email']
    # Check if a user with the same email already exists
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message="that email already exists"), 409
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Create a new User object with the form data
        user = User(username=username, email=email, password=bcrypt.generate_password_hash(password).decode('utf8'))
        # Add the new user to the session
        db.session.add(user)
        db.session.commit()
        # Serialize the user and return as a response
        return UserSchema(exclude=['password']).dump(user), 201

# Route to log in a user
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        # Fetch the user from the database based on the provided email
        stmt = db.select(User).filter_by(email=request.json['email'])
        user = db.session.scalar(stmt)
        # Check if the user exists and the password matches
        if user and bcrypt.check_password_hash(user.password, request.json['password']):
            # Generate an access token for the user
            token = create_access_token(identity=user.email, expires_delta=timedelta(days=1))
            # Serialize the token and user, and return as a response
            return {'token': token, 'user': UserSchema(exclude=['password']).dump(user)}
        else:
            return {'error': 'Invalid email address or password'}, 401
    except KeyError:
        return {'error': 'Email and password are required'}, 400
