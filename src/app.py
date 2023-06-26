from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields
from marshmallow import fields
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from datetime import timedelta, date
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Column, Integer, String, Float
import os
import psycopg2

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://ben:amigo@localhost:5432/bookclub"
app.config['JWT_SECRET_KEY'] = 'friend'



db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

@app.cli.command('db_create')
def db_create(): 
    db.create_all()
    print('Database created successfully')

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped successfully')

@app.cli.command('db_seed')    
def db_seed():
    books = [
        Book(
        title='King James Bible',
        genre='Religion',
        author='Various',
        synopsis="The Old Testament tells the story of God's chosen people, the Hebrews. The New Testament tells of Jesus' birth, life, ministry, death and resurrection, the growth of the early Christian Church, and predictions of the second coming of Jesus.",
        publication_year=1611),
        Book(
        title='The Lord of the Rings',
        genre='High Fantasy',
        author='JRR Tolkien',
        synopsis='In order to defeat the dark lord Sauron, Frodo Baggins is tasked with destroying the one ring',
        publication_year=1954),
        Book(
        title='Dracula',
        genre='Gothic Horror',
        author='Bram Stoker',
        synopsis='Follows the story of Count Dracula, a vampire from Transylvania, as he seeks to spread his curse and terrorize Victorian England.',
        publication_year=1954),
    ]

    db.session.add_all(books)

    test_users = [
        User(
        username='Booklover69',
        email='Booklover69@gmail.com',
        password=bcrypt.generate_password_hash('ilovebooks').decode('utf-8')),
        User(
        username='BenP',
        email='BenP@gmail.com',
        password=bcrypt.generate_password_hash('ayylmao').decode('utf-8'),
        is_admin=True)
    ]
    for user in test_users:
        db.session.add(user)

    db.session.commit()

    reviews = [
        Review(
            review_content="OMG I LOVE THIS BOOK!! SO GOOD!!",
            date_created=date.today(),
            user_id=test_users[0].id,
            book_id=books[1].book_id,
            username=test_users[0].username,
            title=books[1].title,
        )
    ]
    
    db.session.query(Review).delete()
    db.session.add_all(reviews)

    db.session.commit()
    print('Database seeded successfully')
    

    
@app.route("/books", methods=["GET"])
def books():
    books_list = Book.query.all()
    result = books_schema.dump(books_list)
    return jsonify(result)

@app.route("/register", methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test: 
        return jsonify(message="that email already exists"), 409
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=bcrypt.generate_password_hash(password).decode('utf8'))
        db.session.add(user)
        db.session.commit()
        return UserSchema(exclude=['password']).dump(user), 201
    
@app.route('/login', methods=['POST'])
def login():
    try:
        stmt = db.select(User).filter_by(email=request.json['email'])
        user = db.session.scalar(stmt)
        if user and bcrypt.check_password_hash(user.password, request.json['password']):
            token = create_access_token(identity=user.email, expires_delta=timedelta(days=1))
            return {'token': token, 'user': UserSchema(exclude=['password']).dump(user)}
        else:
            return {'error': 'Invalid email address or password'}, 401
    except KeyError:
        return {'error': 'Email and password are required'}, 400


@app.route('/book_details/<int:book_id>', methods=['GET'])
def book_details(book_id: int):
    book = Book.query.filter_by(book_id=book_id).first()
    if book:
        result = book_schema.dump(book)
        return jsonify(result)
    else:
        return jsonify(message="That book does not exist"), 404

@app.route('/add_book', methods=['POST'])
@jwt_required()
def add_book():
    title = request.form['title']
    test = Book.query.filter_by(title=title).first()
    if test:
        return jsonify("There is already a book with that title"), 409
    else:
        genre = request.form['genre']
        author = request.form['author']
        synopsis = request.form['synopsis']
        publication_year = int(request.form['publication_year'])

        new_book = Book(title=title, author=author, genre=genre, synopsis=synopsis, publication_year=publication_year)

        db.session.add(new_book)
        db.session.commit()
        return jsonify(message="You added a new book!"), 201

@app.route('/update_book', methods=['PUT'])
@jwt_required()
def update_book():
    book_id = int(request.form['book_id'])
    book = Book.query.filter_by(book_id=book_id).first()
    if book:
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.synopsis = request.form['synopsis']
        book.publication_year = int(request.form['publication_year'])
        db.session.commit()
        return jsonify(message="You updated a book!"), 202
    else:
        return jsonify(message="Book does not exist"), 404

@app.route('/delete_book/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id: int):
    book = Book.query.filter_by(book_id=book_id).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify(message="You deleted a book"), 202
    else: 
         return jsonify(message="That book does not exist"), 202



    # database models
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    reviews = db.relationship('Review', back_populates='user')

class Book(db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False, unique=True)
    genre = db.Column(db.String, nullable=False)
    synopsis = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

    reviews = db.relationship('Review', back_populates='book')

class Review(db.Model):
    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, primary_key=True)
    review_content = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    username = db.Column(db.String, nullable=False)
    user = db.relationship('User', back_populates='reviews')

    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    book = db.relationship('Book', back_populates='reviews')

class ReviewSchema(ma.Schema):
  user = fields.Nested('UserSchema')
  book = fields.Nested('BookSchema')

  class Meta:
    fields = ('review_id', 'review_content', 'date_created', 'user', 'book')
    ordered = True


class UserSchema(ma.Schema):
    reviews = fields.List(fields.Nested('ReviewSchema'))

    class Meta:
        fields = ('id', 'username', 'email', 'password', 'is_admin', 'reviews')

class BookSchema(ma.Schema):
    reviews = fields.List(fields.Nested('ReviewSchema', only=['review_content']))

    class Meta:
        fields = ('book_id', 'title', 'author', 'genre', 'synopsis', 'publication_year', 'user', 'reviews')

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)


if __name__ == "__main__":
    app.run(debug=True)