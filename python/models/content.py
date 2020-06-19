from datetime import datetime

from db import db

# db.Model binds the class to SQLAlchemy
class ContentModel(db.Model):
    __tablename__ = 'content'

    content_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.section_id'))
    # content_type_id = db.Column(db.Integer, db.ForeignKey('content_type.content_type_id'))
    content_value = db.Column(db.String(100), nullable=True)
    content_description = db.Column(db.Text, nullable=True)
    content_order = db.Column(db.Integer, nullable=True)
    content_creation = db.Column(db.DateTime, nullable=False)
    content_update = db.Column(db.DateTime, nullable=False)

    # contents = db.relationship('ContentModel', lazy='dynamic', cascade="all, delete")

    def __init__(self, section_id, content_value, content_description, content_order, content_creation=datetime.now(), content_update=datetime.now()):
        self.section_id = section_id
        self.content_value = content_value
        self.content_description = content_description
        self.content_order = content_order
        self.content_creation = content_creation    
        self.content_update = content_update

    def json(self):
        return {'content_id': self.content_id, 'section_id': self.section_id, 'content_value': self.content_value, 
                'content_description': self.content_description, 'content_order': self.content_order,
                'content_creation': self.content_creation.strftime('%Y-%m-%d %X'), 
                'content_update': self.content_update.strftime('%Y-%m-%d %X')}

    @classmethod
    def find_by_id(cls, content_id):
        return cls.query.filter_by(content_id=content_id).first()        

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