import datetime
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.book import BookModel

# Inheritance of Resource class
class Book(Resource):
    parser = reqparse.RequestParser()
    # Only arguments added to the parser will retain
    # additional arguments will be removed when parse_args() is called
    # if the request does not contain any added arguments, help message
    # will be returned to the browser instead
    parser.add_argument('description',
        type=str,
        required=False,
        help="This field cannot be left blank!"
    )
    parser.add_argument('genre',
        type=str,
        required=True,
        help="Every book needs a genre."
    )
        
    def get(self, title):
        book = BookModel.find_by_title(title)
        if book:
            return book.json()
        return {'message': 'Book not found'}, 404

    def post(self, title):
        if BookModel.find_by_title(title):
            return {'message': "A book with title '{}' already exists.".format(title)}, 400

        # parse_args() return only arguments added by add_argument as Namespace
        # Any missing added argument will stop and return help message to the browser
        data = Book.parser.parse_args()

        # data namespace is rolled into  one argument (**data)
        book = BookModel(title, **data)

        try:
            book.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return book.json(), 201

    def put(self, title):
        data = Book.parser.parse_args()

        book = BookModel.find_by_title(title)

        if book is None:
            book = BookModel(title, **data)
        else:
            book.description = data['description']
            book.genre = data['genre']

        book.save_to_db()

        return book.json()      

    def delete(self, title):
        book = BookModel.find_by_title(title)
        if book:
            book.delete_from_db()

        return {'message': 'Book deleted'}        

class BookList(Resource):
    def get(self):
        return {'books': [book.json() for book in BookModel.query.all()]}            