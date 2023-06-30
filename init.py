from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
bcrypt = Bcrypt()