from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

# Create a SQLAlchemy instance for database management
db = SQLAlchemy()
# Create a Marshmallow instance for JSON serialization/deserialization
ma = Marshmallow()
# Create a Bcrypt instance for password hashing
bcrypt = Bcrypt()
# Create a JWTManager instance for JSON Web Token management
jwt = JWTManager()
