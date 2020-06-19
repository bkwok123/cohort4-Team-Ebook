from datetime import datetime

from db import db

# db.Model binds the class to SQLAlchemy
class ChapterModel(db.Model):
    __tablename__ = 'chapters'

    chapter_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    chapter_name = db.Column(db.String(100), nullable=True)
    chapter_description = db.Column(db.Text, nullable=True)
    chapter_order = db.Column(db.Integer, nullable=True)
    chapter_creation = db.Column(db.DateTime, nullable=False)
    chapter_update = db.Column(db.DateTime, nullable=False)

    book = db.relationship('BookModel')

    def __init__(self, book_id, chapter_name, chapter_description, chapter_order, chapter_creation=datetime.now(), chapter_update=datetime.now()):
        self.book_id = book_id
        self.chapter_name = chapter_name
        self.chapter_description = chapter_description
        self.chapter_order = chapter_order
        self.chapter_creation = chapter_creation    
        self.chapter_update = chapter_update

    def json(self):
        return {'chapter_id': self.chapter_id, 'book_id': self.book_id, 'chapter_name': self.chapter_name, 
                'chapter_description': self.chapter_description, 'chapter_order': self.chapter_order,
                'chapter_creation': self.chapter_creation.strftime('%Y-%m-%d %X'), 
                'chapter_update': self.chapter_update.strftime('%Y-%m-%d %X')}

    @classmethod
    def find_by_id(cls, chapter_id):
        return cls.query.filter_by(chapter_id=chapter_id).first()        

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()