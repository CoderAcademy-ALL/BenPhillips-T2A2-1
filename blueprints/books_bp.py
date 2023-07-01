from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models.book import Book, BookSchema
from init import db
from blueprints.auth_bp import admin_required

books_bp = Blueprint('books', __name__)

# Route to get all books
@books_bp.route("/books", methods=["GET"])
def books():
     # Select all books from the database and order them by book_id
    stmt = db.select(Book).order_by(Book.book_id.asc())
      # Execute the query and fetch all the books
    books = db.session.scalars(stmt).all()
      # Serialize the books using BookSchema and return as a response
    return BookSchema(many=True).dump(books)

# Route to get details of a specific book
@books_bp.route('/book_details/<int:book_id>', methods=['GET'])
def book_details(book_id: int):
  # Select a book with the given book_id
  stmt = db.select(Book).filter_by(book_id=book_id)
   # Fetch the book
  book = db.session.scalar(stmt)
  if book:
     # Serialize the book using BookSchema and return as a response
    return BookSchema().dump(book)
  else:
    return {'error': 'Book not found'}, 404
    
# Route to add a new book
@books_bp.route('/add_book', methods=['POST'])
@jwt_required()
def add_book():
    # Get the form data
    title = request.form['title']
     # Check if a book with the same title already exists
    book = Book.query.filter_by(title=title).first()
    if book:
        return jsonify("There is already a book with that title"), 409
    else:
        genre = request.form['genre']
        author = request.form['author']
        synopsis = request.form['synopsis']
        publication_year = int(request.form['publication_year'])
 # Create a new Book object
        new_book = Book(title=title, author=author, genre=genre, synopsis=synopsis, publication_year=publication_year)
# Add the new book to the session
        db.session.add(new_book)
        db.session.commit()
        return jsonify(message="You added a new book!"), 201
# Route to update an existing book
@books_bp.route('/update_book', methods=['PUT'])
@jwt_required()
def update_book():
    # Get the form data
    book_id = int(request.form['book_id'])
    # Find the book with the given book_id
    book = Book.query.filter_by(book_id=book_id).first()
    if book:
        admin_required()
        # Update the book's attributes with the form data
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.synopsis = request.form['synopsis']
        book.publication_year = int(request.form['publication_year'])
        # Commit the changes to the database
        db.session.commit()
        return jsonify(message="You updated a book!"), 202
    else:
        return jsonify(message="Book does not exist"), 404

# Route to delete a book
@books_bp.route('/delete_book/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id: int):
    # Find the book with the given book_id
    book = Book.query.filter_by(book_id=book_id).first()
    if book:
        admin_required()
        # Delete the book from the session
        db.session.delete(book)
        db.session.commit()
        return jsonify(message="You deleted a book"), 202
    else:
        return jsonify(message="That book does not exist"), 202