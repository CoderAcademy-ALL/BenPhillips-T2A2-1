from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields
from marshmallow import fields
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta, date
from collections import OrderedDict
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from os import environ
from models.user import User, UserSchema
from models.book import Book, BookSchema
from models.comment import Comment, CommentSchema
from models.review import Review, ReviewSchema
from init import db, ma, bcrypt, jwt

from blueprints.cli_bp import cli_bp
from blueprints.auth_bp import auth_bp
from blueprints.books_bp import books_bp
from blueprints.comments_bp import comments_bp
from blueprints.reviews_bp import reviews_bp

def create_app():
    # Create a Flask application instance
    app = Flask(__name__)

    # Configure the SQLAlchemy database URI from environment variables
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URI')

    # Configure the JWT secret key from environment variables
    app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')

    # Initialize the SQLAlchemy database
    db.init_app(app)

    # Initialize the Marshmallow serializer/deserializer
    ma.init_app(app)

    # Initialize the Flask-JWT-Extended extension
    jwt.init_app(app)

    # Initialize the Flask-Bcrypt extension for password hashing
    bcrypt.init_app(app)

    # Register the blueprints for different parts of the application
    app.register_blueprint(cli_bp)  # CLI blueprint
    app.register_blueprint(auth_bp)  # Authentication blueprint
    app.register_blueprint(books_bp)  # Books blueprint
    app.register_blueprint(comments_bp)  # Comments blueprint
    app.register_blueprint(reviews_bp)  # Reviews blueprint

    return app
