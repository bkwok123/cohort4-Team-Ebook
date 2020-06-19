from datetime import datetime
from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required

from models.section import SectionModel

# Inheritance of Resource class
class Section(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('chapter_id',
        type=int,
        required=True,
        help="Every section needs a chapter id."
    )    
    parser.add_argument('section_name',
        type=str,
        required=False,
        help="Every section needs a name."
    )
    parser.add_argument('section_description',
        type=str,
        required=False,
        help="Every section needs a description."
    )
    parser.add_argument('section_order',
        type=int,
        required=False,
        help="Every section needs an order."
    )
        
    def get(self, section_id):
        section = SectionModel.find_by_id(section_id)
        if section:
            return section.json()
        return {'message': 'Section not found'}, 404

    def post(self):        
        data = Section.parser.parse_args()
        section = SectionModel(**data)

        try:
            section.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return section.json(), 201

    def put(self, section_id):
        data = Section.parser.parse_args()

        section = SectionModel.find_by_id(section_id)

        if section is None:
            section = SectionModel(**data)
        else:
            section.chapter_id = data['chapter_id']
            section.section_name = data['section_name']
            section.section_description = data['section_description']
            section.section_order = data['section_order']
            section.section_update = datetime.now()

        section.save_to_db()

        return section.json()      

    def delete(self, section_id):
        section = SectionModel.find_by_id(section_id)
        if section:
            section.delete_from_db()

        return {'message': 'Section deleted'}        

class SectionList(Resource):
    def get(self):        
        return {'sections': [section.json() for section in SectionModel.query.all()]}

    # Delete all sections will not delete child items
    def delete(self):
        SectionModel.delete_all()        
        return {'message': 'All sections deleted'}