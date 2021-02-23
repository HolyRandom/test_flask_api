from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import os
from dotenv import load_dotenv


app = Flask(__name__)
api = Api(app)
load_dotenv()
use_db = os.getenv('USE_DB')
if use_db == "True":
    driver = os.getenv('SQL_DRIVER')
    db_name = os.getenv('DBNAME')
    db_user = os.getenv('USER')
    db_password = os.getenv('PASSWORD')
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    sql_config = f'{driver}://{db_user}:{db_password}@{host}:{port}/{db_name}'
    app.config['SQLALCHEMY_DATABASE_URI'] = sql_config
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)



class Storage:
    """Class of storage logic"""
    def __init__(self):
        self.storage = factory

    def storage_method(self, method, user_id=None, name=None):
        if method == 'GET':
            return self.storage.get(user_id)
        elif method == 'POST':
            return self.storage.post(name)
        elif method == 'PUT':
            return self.storage.put(user_id, name)
        elif method == 'DELETE':
            return self.storage.delete(user_id)

class StorageFactory:
    def get_storage(self):
        if use_db:
            return DataBase()
        else:
            return Memory()


class Memory():
    """Methods for work in memory"""
    def __init__(self):
        self._users = []


    def post(self, name):
        try:
            self.max_id = max(x['id'] for x in self._users)
        except ValueError:
            self.max_id = 0
        self.result = self._users.append({'id': self.max_id + 1, 'name': name})
        return self.result

    def get(self, user_id):
        self.result = (x for x in self._users if x['id'] == user_id)
        return self.result

    def put(self, user_id, name):
        self.index = next((x for x in self._users if x['id'] == user_id), None)
        print(name)
        self._users[self.index]['name'] = name
        return self._users[self.index]

    def delete(self, user_id):
        self.index, _ = next((x for x in enumerate(self._users) if x[1]['id'] == user_id), (None, None))
        self.result = self._users.pop(self.index)
        return self.result


class DataBase():
    """Methods for work with Database"""

    def post(self, name):
        max_id = db.session.query(func.max(UserModel.id)).scalar()  # Check maximum value id in table
        if max_id == None:
            user = UserModel(id=1, name=name)
        else:
            user = UserModel(id=max_id + 1, name=name)
        db.session.add(user)
        result = db.session.commit()
        return result

    def get(self, user_id):
        result = UserModel.query.filter_by(id=user_id).first()
        return result

    def put(self, user_id, name):
        user = db.session.query(UserModel).filter(UserModel.id == user_id).first()  # check user id in table
        if not user:
            abort(409, message='User is not created')
        else:
            db.session.query(UserModel).filter(UserModel.id == user_id).update({'id': user_id,
                                                                                     'name': name})
            result = db.session.commit()
            return result

    def delete(self, user_id):
        db.session.query(UserModel).filter(UserModel.id == user_id).delete()
        result = db.session.commit()
        return result



class UserModel(db.Model):
    '''Create database model'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"ID(id = {id}, name = {name})"

db.create_all()

user_args = reqparse.RequestParser()  # Parse args in http methods
user_args.add_argument('name', type=str)

resource_field = {
    'id': fields.Integer,
    'name': fields.String
}


def abort_name():
    abort(409, message='Need send "name" data')


class UserPost(Resource):
    @marshal_with(resource_field)
    def post(self):
        arg = user_args.parse_args()
        name = arg['name']
        if name == None:
            abort_name()
        result = Storage().storage_method(method="POST", name=name)
        return result


class UserRUD(Resource):

    @marshal_with(resource_field)
    def get(self, user_id):
        result = Storage().storage_method(method="GET", user_id=user_id)
        return result

    @marshal_with(resource_field)
    def put(self, user_id):
        arg = user_args.parse_args()
        name = arg['name']
        if name == None:
            abort_name()

        result = Storage().storage_method(method="PUT", user_id=user_id, name=name)
        return result, 201

    @marshal_with(resource_field)
    def delete(self, user_id):
        Storage().storage_method(method="DELETE", user_id=user_id)
        return '', 202


api.add_resource(UserPost, "/api/user")
api.add_resource(UserRUD, "/api/user/<int:user_id>")


if __name__ == "__main__":
    factory = StorageFactory().get_storage()
    app.run(debug=True)
