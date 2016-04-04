from flask import request, jsonify
from flask_restful import Resource, abort
from sqlalchemy.exc import DataError
from sqlalchemy.orm.exc import NoResultFound

from flaskapp import app, db
from flaskapp.main.models import Restroom
from flaskapp.main.resources.schemas.restroom import RestroomSchema


class RestroomsAPI(Resource):
    """GET All Restrooms"""

    def get(self):
        try:
            q = Restroom.query

            restrooms = q.all()

            if restrooms:
                return RestroomSchema(many=True).dump(restrooms).data
            else:
                abort(app.config['NOT_FOUND'], message=app.config['RESTROOM_NOT_FOUND'])
        except(DataError, NoResultFound):
            abort(app.config['NOT_FOUND'], message=app.config['RESTROOM_NOT_FOUND'])


class RestroomAPI(Resource):
    """GET a specific Restroom"""

    def get(self, id):
        try:
            restroom = Restroom.query.get(id)
            if restroom:
                return RestroomSchema().dump(restroom).data
            else:
                abort(app.config['NOT_FOUND'], message=app.config['RESTROOM_NOT_FOUND'])
        except(DataError, NoResultFound):
            abort(app.config['NOT_FOUND'], message=app.config['RESTROOM_NOT_FOUND'])
