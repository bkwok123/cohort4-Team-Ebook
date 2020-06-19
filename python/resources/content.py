from datetime import datetime
from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required

from models.content import ContentModel

# Inheritance of Resource class
class Content(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('section_id',
        type=int,
        required=True,
        help="Every content needs a section id."
    )    
    parser.add_argument('content_value',
        type=str,
        required=False,
        help="Every content needs a value."
    )
    parser.add_argument('content_description',
        type=str,
        required=False,
        help="Every content needs a description."
    )
    parser.add_argument('content_order',
        type=int,
        required=False,
        help="Every content needs an order."
    )
        
    def get(self, content_id):
        content = ContentModel.find_by_id(content_id)
        if content:
            return content.json()
        return {'message': 'Content not found'}, 404

    def post(self):        
        data = Content.parser.parse_args()
        content = ContentModel(**data)

        try:
            content.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return content.json(), 201

    def put(self, content_id):
        data = Content.parser.parse_args()

        content = ContentModel.find_by_id(content_id)

        if content is None:
            content = ContentModel(**data)
        else:
            content.section_id = data['section_id']
            # content.content_type_id = data['content_type_id']
            content.content_value = data['content_value']
            content.content_description = data['content_description']
            content.content_order = data['content_order']
            content.content_update = datetime.now()

        content.save_to_db()

        return content.json()      

    def delete(self, content_id):
        content = ContentModel.find_by_id(content_id)
        if content:
            content.delete_from_db()

        return {'message': 'Content deleted'}        

class ContentList(Resource):
    def get(self):        
        return {'contents': [content.json() for content in ContentModel.query.all()]}

    # Delete all contents will not delete child items
    def delete(self):
        ContentModel.delete_all()        
        return {'message': 'All contents deleted'}