from flask import request, jsonify
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import DataError
from flaskapp.main.resources.models import Restroom
from flaskapp import app, db
from flaskapp.main.resources.schemas.restroom import RestroomSchema


class HelloWorld(Resource):
    """Test Call"""

    def get(self):
        return 'Hello World'