from flask import Flask
from flask_restful import Api, reqparse

from resources.student import Student, StudentList
from resources.classroom import Classroom, ClassroomList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Student, '/student/<string:name>')
api.add_resource(StudentList, '/students')
api.add_resource(Classroom, '/classroom/<string:name>')
api.add_resource(ClassroomList, '/classrooms')

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)