from datetime import datetime


from db import db
class SectionModel(db.Model):
    __tablename__ = 'sections'

    section_id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.chapter_id'))
    section_name = db.Column(db.String(100), nullable=True)
    section_description = db.Column(db.Text, nullable=True)
    section_order = db.Column(db.Integer, nullable=True)
    section_creation = db.Column(db.DateTime, nullable=False)
    section_update = db.Column(db.DateTime, nullable=False)

    # contents = db.relationship('ContentModel', lazy='dynamic', cascade="all, delete")

    def __init__(self, chapter_id, section_name, section_description, section_order, section_creation=datetime.now(), section_update=datetime.now()):
        self.chapter_id = chapter_id
        self.section_name = section_name
        self.section_description = section_description
        self.section_order = section_order
        self.section_creation = section_creation    
        self.section_update = section_update

    def json(self):
        return {'section_id': self.section_id, 'chapter_id': self.chapter_id, 'section_name': self.section_name, 
                'section_description': self.section_description, 'section_order': self.section_order,
                'section_creation': self.section_creation.strftime('%Y-%m-%d %X'), 
                'section_update': self.section_update.strftime('%Y-%m-%d %X')}

    @classmethod
    def find_by_id(cls, section_id):
        return cls.query.filter_by(section_id=section_id).first()        


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
