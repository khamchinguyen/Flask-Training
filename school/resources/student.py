from tokenize import String
from flask_restful import Resource, reqparse
from models.student import StudentModel

class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('major',
        type=String,
        required=True,
        help="Every student needs a major"
    )
    parser.add_argument('class_id',
        type=int,
        required=True,
        help="Every students needs a class id."
    )

    def get(self, name):
        student = StudentModel.find_by_name(name)
        if student:
            return student.json()
        return {'message': 'Student not found'}, 404
            
    def post(self, name):
        if StudentModel.find_by_name(name):
            return {'message': "A student with name '{}' already exists.".format(name)}, 400
        
        data = Student.parser.parse_args()

        student = StudentModel(name, **data)
        try:
            student.save_to_db()
        except:
            return {'message': ' An error occured inserting the student'}, 500 
        
        return student.json(), 201

    def delete(self, name):
        student = StudentModel.find_by_name(name)
        if student:
            student.delete_from_db()
            return {'message': 'Student deleted'}
        return {'message': 'Student not found'}, 404

    def put(self, name):
        data = Student.parser.parse_args()
        student = StudentModel.find_by_name(name)

        if student:
            student.price = data['price']
        else:
            item = StudentModel(name, **data)
        
        item.save_to_db()
        return item.json()


class StudentList(Resource):
    def get(self):
        return {'students': [student.json() for student in StudentModel.query.all()]}