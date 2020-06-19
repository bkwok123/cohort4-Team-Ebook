from datetime import datetime

from db import db

# db.Model binds the class to SQLAlchemy
class SectionModel(db.Model):
    __tablename__ = 'sections'

    section_id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.chapter_id'))
    section_name = db.Column(db.String(100))
    section_description = db.Column(db.Text)
    section_order = db.Column(db.String(100))
    section_creation = db.Column(db.DateTime)
    section_update = db.Column(db.DateTime)

    content = db.relationship('ContentModel', lazy='dynamic', cascade="all, delete")

    def __init__(self, section_name, section_description, section_order, section_creation=datetime.now(), section_update=datetime.now()):
        self.section_name = section_name
        self.section_description = section_description
        self.section_order = section_order
        self.section_creation = section_creation
        self.section_update = section_update

    def json(self):
        return {'section_id': self.section_id, 'section_name': self.section_name, 'section_description': self.section_description, 
            'section_order': self.section_order, 'content': [content.json() for content in self.content.all()],
            'section_creation': self.section_creation.strftime('%Y-%m-%d %X'), 
            'section_update': self.section_update.strftime('%Y-%m-%d %X')}

    @classmethod
    def find_by_id(cls, section_id):
        return cls.query.filter_by(section_id=section_id).first()   