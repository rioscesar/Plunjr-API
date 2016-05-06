import copy

from flask import request, jsonify
from flask_restful import Resource, abort, reqparse
from sqlalchemy import func, text
from sqlalchemy.exc import DataError
from sqlalchemy.orm.exc import NoResultFound

from flaskapp import app, db
from flaskapp.main.models import Restroom
from flaskapp.main.resources.schemas.restroom import RestroomSchema

import logging

logger = logging.getLogger(__name__)


class RestroomsAPI(Resource):
    """GET All Restrooms"""

    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('lat', location='args', type=float)
        self.reqparser.add_argument('lng', location='args', type=float)
        self.reqparser.add_argument('radius', location='args', type=float)

    def get(self):
        try:
            logger.info('Inside get all rrs for RESTROOMSAPI!')
            args = self.reqparser.parse_args()
            lat = args['lat']
            lng = args['lng']
            radius = args['radius'] if args['radius'] is not None else 5000

            logger.info('lat is: {} and lng is: {} and radius is: {}'.format(lat, lng, radius))

            q = Restroom.query

            q = self.get_restrooms_near_me(q, lat, lng, radius)
            logger.info('Nothing wrong, about to get all restrooms in this radius')
            restrooms = q.all()
        except(DataError, NoResultFound, Exception) as e: #
            return []

        return RestroomSchema(many=True).dump(restrooms).data

    def get_restrooms_near_me(self, q, lat, lng, radius_in_meters):
        logger.info('GET_RESTROOMS_NEAR_ME')

        sql = text('earth_box( ll_to_earth({}, {}), {}) @> ll_to_earth(restrooms.lat, restrooms.lng)'
                   .format(lat, lng, radius_in_meters))

        q = q.filter(sql)
        logger.info('About to return query from GET_RESTROOMS_NEAR_ME')
        return q



class RestroomAPI(Resource):
    """GET a specific Restroom"""

    def get(self, id):
        try:
            restroom = Restroom.query.get(id)
            if restroom:
                return RestroomSchema().dump(restroom).data
        except(DataError, NoResultFound):
            abort(app.config['NOT_FOUND'], message=app.config['RESTROOM_NOT_FOUND'])

        return []

    def patch(self, id):
        logger.info('Inside PATCH')
        try:
            request.json['id'] = id
            rr, errors = RestroomSchema(partial=True, exclude=('imagesUrl',)).load(request.json)
            logger.info('restroom just got loaded')
            if errors:
                logger.info('There was an error')
                abort(app.config['UNPROCESSABLE_ENTITY'], message=jsonify(errors))
            if request.json['imagesUrl']:
                image_array = copy.deepcopy(rr.images_url)
                image_array += request.json['imagesUrl']
                rr.images_url = image_array
            db.session.add(rr)
            db.session.commit()
            logger.info('images got commited')
            return RestroomSchema().dump(rr).data
        except(DataError, NoResultFound):
            abort(app.config['NOT_FOUND'], message=app.config['RESTROOM_NOT_FOUND'])
