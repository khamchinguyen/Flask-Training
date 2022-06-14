from flask_restful import Resource, reqparse
from models.classroom import ClassroomModel

class Classroom(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('teacher',
        type=str,
        required=True,
        help="Every class needs a teacher."
    )
    
    def get(self, name):
        classroom = ClassroomModel.find_by_name(name)
        if classroom:
            return classroom.json()
        return {'message': 'Classroom not found'}, 404

    def post(self, name):
        if ClassroomModel.find_by_name(name):
            return {'message': "A classroom with name '{}' already exists.".format(name)}, 400

        data = Classroom.parser.parse_args()

        classroom = ClassroomModel(name, **data)
        try:
            classroom.save_to_db()
        except:
            return {'message': 'An error occured while creating the store.'}, 500
        
        return classroom.json(), 201

    def delete(self, name):
        classroom = ClassroomModel.find_by_name(name)
        if classroom:
            classroom.delete_from_db()
        return {'message': 'Classroom deleted'}

    def put(self, name):
        data = Classroom.parser.parse_args()
        classroom = Classroom.find_by_name(name)

        if classroom:
            classroom.teacher = data['teacher']
        else:
            item = ClassroomModel(name, **data)
        
        item.save_to_db()
        return item.json()

class ClassroomList(Resource):
    def get(self):
        return {'classrooms': [classroom.json() for classroom in ClassroomModel.query.all()]}