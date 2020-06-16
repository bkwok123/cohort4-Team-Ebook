from datetime import datetime

from db import db

# db.Model binds the class to SQLAlchemy
class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    genre = db.Column(db.String(100))
    creation = db.Column(db.DateTime)
    update = db.Column(db.DateTime)

    # All class property names must match to column defined above 
    # to save the information to the database
    # Additional unmatched properties will not save in the database columns
    def __init__(self, title, description, genre, creation=datetime.now(), update=datetime.now()):
        self.title = title
        self.description = description
        self.genre = genre
        self.creation = creation
        self.update = update    

    def json(self):
        return {'title': self.title, 'description': self.description, 
                'genre': self.genre, 'creation': self.creation.strftime('%Y/%m/%d %X'), 
                'update': self.update.strftime('%Y/%m/%d %X')}

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()