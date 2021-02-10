from flask import Flask
from flask_restful import Api, Resource, reqparse, fields,  marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import os
from dotenv import load_dotenv


app = Flask(__name__)
api = Api(app)


# Load  environment variables and select SQLAlchemy Driver
load_dotenv()
use_db = os.getenv('USE_DB')
if use_db == True:
    print(use_db)
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

class UserModel(db.Model):
    '''Create database model'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"ID(id = {id}, name = {name})"


db.create_all() #Create all model


user_args = reqparse.RequestParser()  # Parse args in http methods
user_args.add_argument('name', type=str)

resource_field= {
    'id': fields.Integer,
    'name': fields.String
}

def abort_name():
    abort(409, message='Need send "name" data')


class UserPost(Resource):
    @marshal_with(resource_field)
    def post(self):
        arg = user_args.parse_args()
        if arg['name'] == None:
            abort_name()
        max_id = db.session.query(func.max(UserModel.id)).scalar()  # Check maximum value id in table
        if max_id == None:
            user = UserModel(id=1, name=arg['name'])
        else:
            user = UserModel(id=max_id + 1, name=arg['name'])
        db.session.add(user)
        db.session.commit()
        return user


class User(Resource):
    @marshal_with(resource_field)
    def get(self, user_id):
        result = UserModel.query.filter_by(id=user_id).first()
        return result

    @marshal_with(resource_field)
    def put(self,  user_id):
        arg = user_args.parse_args()
        if arg['name'] == None:
            abort_name()
        user = db.session.query(UserModel).filter(UserModel.id == user_id).first()  # check user id in table
        if not user:
            abort(409, message='User is not created')
        else:
            db.session.query(UserModel).filter(UserModel.id == user_id).update({'id': user_id,
                                                                                'name': arg['name']})
            db.session.commit()
        return '', 201

    @marshal_with(resource_field)
    def delete(self, user_id):
        db.session.query(UserModel).filter(UserModel.id == user_id).delete()
        db.session.commit()
        return '', 202


api.add_resource(UserPost, "/api/user")
api.add_resource(User, "/api/user/<int:user_id>")

if __name__ == '__main__':
    app.run(debug=True)
