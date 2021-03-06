from datetime import datetime

from db import db

# db.Model binds the class to SQLAlchemy
class BookModel(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(100))
    book_description = db.Column(db.Text)
    book_genre = db.Column(db.String(100))
    book_creation = db.Column(db.DateTime)
    book_update = db.Column(db.DateTime)

    chapters = db.relationship('ChapterModel', lazy='dynamic', cascade="all, delete")

    # All class property names must match to column defined above 
    # to save the information to the database
    # Additional unmatched properties will not save in the database columns
    def __init__(self, book_title, book_description, book_genre, book_creation=datetime.now(), book_update=datetime.now()):
        self.book_title = book_title
        self.book_description = book_description
        self.book_genre = book_genre
        self.book_creation = book_creation
        self.book_update = book_update    

    def json(self):
        return {'book_id': self.book_id, 'book_title': self.book_title, 'book_description': self.book_description, 
                'book_genre': self.book_genre, 'chapters': [chapter.json() for chapter in self.chapters.all()],
                'book_creation': self.book_creation.strftime('%Y-%m-%d %X'), 
                'book_update': self.book_update.strftime('%Y-%m-%d %X')}

    @classmethod
    def find_by_id(cls, book_id):
        return cls.query.filter_by(book_id=book_id).first()        

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def delete_all(cls):
        db.session.query(cls).delete()
        db.session.commit()        

    @classmethod
    def query_all(cls):
        result = db.session.query(cls.book_id, cls.book_title, cls.book_description, 
                                  cls.book_genre, cls.book_creation, cls.book_update).all()

        return [{"book_id": book.book_id, "book_title": book.book_title,
                 "book_description": book.book_description, "book_genre": book.book_genre,
                 "book_creation": book.book_creation.strftime('%Y-%m-%d %X'), 
                 "book_update": book.book_update.strftime('%Y-%m-%d %X')} for book in result]
