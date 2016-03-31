
from flask import request, jsonify
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import DataError
from flaskapp.main.resources.models import Restroom
from flaskapp import app, db
from flaskapp.main.resources.schemas.restroom import RestroomSchema


class RestroomsAPI(Resource):
    """GET All Restrooms or POST a restroom"""

    def get(self):
        try:
            q = Restroom.query

            count = q.count()
            restrooms = q.all()

            if restrooms:
                restrooms = RestroomSchema(many=True).dump(restrooms).data
                return jsonify(
                    {
                        'count': count,
                        'results': restrooms
                    }
                )
            else:
                abort(app.config['NOT_FOUND'], message=app.config['RESTROOM_NOT_FOUND'])
        except(DataError, NoResultFound):
            abort(app.config['NOT_FOUND'], message=app.config['RESTROOM_NOT_FOUND'])

        pass

    def post(self):
        discussion, errors = RestroomSchema().load(request.json)

        if errors:
            abort(app.config['UNPROCESSABLE_ENTITY'], message=jsonify(errors))

        db.session.add(discussion)
        db.session.commit()

        restroom_dump, errors = RestroomSchema().dump(discussion)

        if errors:
            abort(app.config['UNPROCESSABLE_ENTITY'], message=jsonify(errors))

        return restroom_dump


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
