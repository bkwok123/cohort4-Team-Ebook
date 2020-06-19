from datetime import datetime
from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required

from models.chapter import ChapterModel

# Inheritance of Resource class
class Chapter(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('book_id',
        type=int,
        required=True,
        help="Every chapter needs a book id."
    )    
    parser.add_argument('chapter_name',
        type=str,
        required=False,
        help="Every chapter needs a name."
    )
    parser.add_argument('chapter_description',
        type=str,
        required=False,
        help="Every chapter needs a description."
    )
    parser.add_argument('chapter_order',
        type=int,
        required=False,
        help="Every chapter needs an order."
    )
        
    def get(self, chapter_id):
        chapter = ChapterModel.find_by_id(chapter_id)
        if chapter:
            return chapter.json()
        return {'message': 'Chapter not found'}, 404

    def post(self):        
        data = Chapter.parser.parse_args()
        chapter = ChapterModel(**data)

        try:
            chapter.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return chapter.json(), 201

    def put(self, chapter_id):
        data = Chapter.parser.parse_args()

        chapter = ChapterModel.find_by_id(chapter_id)

        if chapter is None:
            chapter = ChapterModel(**data)
        else:
            chapter.book_id = data['book_id']
            chapter.chapter_name = data['chapter_name']
            chapter.chapter_description = data['chapter_description']
            chapter.chapter_order = data['chapter_order']
            chapter.chapter_update = datetime.now()

        chapter.save_to_db()

        return chapter.json()      

    def delete(self, chapter_id):
        chapter = ChapterModel.find_by_id(chapter_id)
        if chapter:
            chapter.delete_from_db()

        return {'message': 'Chapter deleted'}        

class ChapterList(Resource):
    def get(self):        
        return {'chapters': [chapter.json() for chapter in ChapterModel.query.all()]}