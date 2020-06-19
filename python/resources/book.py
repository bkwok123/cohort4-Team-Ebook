from datetime import datetime
from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required

from models.book import BookModel

# Inheritance of Resource class
class Book(Resource):
    parser = reqparse.RequestParser()
    # Only arguments added to the parser will retain
    # additional arguments will be removed when parse_args() is called
    # if the request does not contain any added arguments, help message
    # will be returned to the browser instead
    parser.add_argument('book_title',
        type=str,
        required=True,
        help="Every book needs a title."
    )    
    parser.add_argument('book_description',
        type=str,
        required=False,
        help="Every book needs a description."
    )
    parser.add_argument('book_genre',
        type=str,
        required=False,
        help="Every book needs a genre."
    )
        
    def get(self, book_id):
        book = BookModel.find_by_id(book_id)
        if book:
            return book.json()
        return {'message': 'Book not found'}, 404

    def post(self):        
        # parse_args() return only arguments added by add_argument as Namespace
        # Any missing added argument will stop and return help message to the browser
        data = Book.parser.parse_args()

        # data namespace is rolled into one argument (**data)
        book = BookModel(**data)

        try:
            book.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return book.json(), 201

    def put(self, book_id):
        data = Book.parser.parse_args()

        book = BookModel.find_by_id(book_id)
        
        if book is None:    # Create a new book if it does not exist in the database
            book = BookModel(**data)
        else:               # Update the book if it exists in the database
            book.book_title = data['book_title']
            book.book_description = data['book_description']
            book.book_genre = data['book_genre']
            book.book_update = datetime.now()

        book.save_to_db()

        return book.json()      

    # Delete a book will delete all child items
    def delete(self, book_id):
        book = BookModel.find_by_id(book_id)
        if book:
            book.delete_from_db()

        return {'message': 'Book deleted'}        

class BookList(Resource):
    # use query.with_entities(DataModel.col1, DataModel.col2) for a specific columns
    def get(self):        
        # return {'books': [book.json() for book in BookModel.query.all()]}            
        return {'books': BookModel.query_all()}
    
    # Delete all books will not delete child items
    def delete(self):
        BookModel.delete_all()        
        return {'message': 'All books deleted'}