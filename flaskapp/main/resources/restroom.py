from flask_restful import Resource, abort, reqparse
from sqlalchemy import func
from sqlalchemy.exc import DataError
from sqlalchemy.orm.exc import NoResultFound

from flaskapp import app, db
from flaskapp.main.models import Restroom
from flaskapp.main.resources.schemas.restroom import RestroomSchema


class RestroomsAPI(Resource):
    """GET All Restrooms"""

    def __init__(self, *args, **kwargs):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('lat', location='args', type=float)
        self.reqparser.add_argument('lng', location='args', type=float)
        self.reqparser.add_argument('radius', location='args', type=float)

    def get(self):
        try:
            print('inside restrooms api')
            args = self.reqparser.parse_args()
            lat = args['lat']
            lng = args['lng']
            radius = args['radius'] if args['radius'] is not None else 8046.72
            print('got lat: ', lat, ', got lng: ', lng)
            q = Restroom.query

            q = self.get_restrooms_near_me(q, lat, lng, radius)

            restrooms = q.all()

            if restrooms:
                return RestroomSchema(many=True).dump(restrooms).data
            else:
                abort(app.config['NOT_FOUND'], message=app.config['RESTROOM_NOT_FOUND'])
        except(DataError, NoResultFound):
            abort(app.config['NOT_FOUND'], message=app.config['RESTROOM_NOT_FOUND'])

    def get_restrooms_near_me(self, q, lat, lng, radius_in_meters):

        where_am_i = func.ll_to_earth(lat, lng)
        q = q.filter(func.earth_box(where_am_i, radius_in_meters)
                     >=
                     func.ll_to_earth(Restroom.lat, Restroom.lng))

        return q


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
