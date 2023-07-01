from flask import Blueprint
from datetime import date
from models.user import User
from models.book import Book
from models.comment import Comment
from models.review import Review
from init import db, bcrypt

#  Create a Blueprint named 'cli_bp' to define CLI commands related to the database
cli_bp = Blueprint('db', __name__)

# CLI command to create the database
@cli_bp.cli.command('db_create')
def db_create():
    # Drop all existing tables from the database
    db.drop_all() 
     # Create all tables based on the defined models
    db.create_all()
    print('Database created successfully')

# CLI command to seed the database with initial data
@cli_bp.cli.command('db_seed')    
def db_seed():
     # Create some Book objects with initial data
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
        publication_year=1899),
    ]
 # Add the Book objects to the session
    db.session.add_all(books)
 # Create some User objects with initial data
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
    # Add the User objects to the session
    for user in test_users:
        db.session.add(user)
 # Commit the changes to the database
    db.session.commit()
 # Create some Review objects with initial data
    reviews = [
        Review(
            review_content="OMG I LOVE THIS BOOK!! SO GOOD!!",
            date_created=date.today(),
            user=test_users[0],
            book=books[1],
            username=test_users[0].username,
            title=books[1].title
        ),
        Review(
            review_content="Greatest book of all time",
            date_created=date.today(),
            user=test_users[1],
            book=books[0],
            username=test_users[1].username,
            title=books[0].title
        )
    ]
  # Add the Review objects to the session
    db.session.add_all(reviews)
    db.session.commit()
  # Create some Comment objects with initial data
    comments = [
        Comment(
            comment_content="I disagree with you, my boy",
            date_created=date.today(),
            user=test_users[1],
            review=reviews[1],
            username=test_users[1].username
        )
    ]
 # Add the Comment objects to the session
    db.session.add_all(comments)
    db.session.commit()
# Print message to indicate cli command was successful
    print('Database seeded successfully')