from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
import psycopg2

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://DonQuixote:Sancho@localhost:5432/bookclub"

db = SQLAlchemy(app)

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
    db.session.commit()

    test_user = User(
        username='Booklover69',
        email='Booklover69@gmail.com',
        password='ilovebooks')

    db.session.add(test_user)
    db.session.commit()
    print('Database seeded successfully')

@app.route('/')
def hello_world():
    return 'ayup world'

@app.route('/supersimple')
def supersimple():
    return jsonify(message='supersimple supersimple'), 200

@app.route('/notfound')
def notfound():
    return jsonify(message='not found blud'), 404

@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message="sorry ur not old enough"), 401 
    else:
        return jsonify(message="welcome u good blud"), 400

@app.route('/URLvariables/<string:name>/<int:age>')
def URLvariables(name: str, age: int):
    if age < 18:
        return jsonify(message="sorry ur not old enough"), 401 
    else:
        return jsonify(message="welcome u good blud"), 400
    
    # database models
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Book(db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False, unique=True)
    genre = db.Column(db.String, nullable=False)
    synopsis = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)




if __name__ == '__main__':
    app.run()