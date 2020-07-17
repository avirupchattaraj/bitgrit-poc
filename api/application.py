from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList
from flask import request
import os

file_path = os.path.abspath(os.getcwd())+"/users.db"

# Create a new Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Set up SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)

# Define a class for the User table
class UserBigFive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    personality = db.Column(db.String)

# Create the table
db.create_all()

# Create data abstraction layer
class UserBigFiveSchema(Schema):
    class Meta:
        type_ = 'user'
        self_view = 'user_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'user_many'

    id = fields.Integer()
    name = fields.Str(required=True)
    personality = fields.Str(required=True)


# Create resource managers and endpoints
class UserBigFiveMany(ResourceList):
    schema = UserBigFiveSchema
    data_layer = {'session': db.session,
                  'model': UserBigFive}

class UserBigFiveOne(ResourceDetail):
    schema = UserBigFiveSchema
    data_layer = {'session': db.session,
                  'model': UserBigFive}

api = Api(app)
api.route(UserBigFiveMany, 'user_many', '/users')
api.route(UserBigFiveOne, 'user_one', '/users/<int:id>')

# main loop to run app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
