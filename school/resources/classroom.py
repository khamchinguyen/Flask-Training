from flask_restful import Resource
from models.classroom import ClassroomModel

class Classroom(Resource):
    def get(self, name):
        classroom = ClassroomModel.find_by_name(name)
        if classroom:
            return classroom.json()
        return {'message': 'Classroom not found'}, 404

    def post(self, name):
        if ClassroomModel.find_by_name(name):
            return {'message': "A classroom with name '{}' already exists.".format(name)}, 400

        classroom = ClassroomModel(name)
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

class ClassroomList(Resource):
    def get(self):
        return {'classrooms': [classroom.json() for classroom in ClassroomModel.query.all()]}