from flask import request, jsonify
from flask_restful import Resource, abort
from sqlalchemy import and_
from sqlalchemy.exc import DataError
from sqlalchemy.orm.exc import NoResultFound

from flaskapp import app, db
from flaskapp.main.models import Review, Restroom
from flaskapp.main.resources.schemas.restroom import RestroomSchema
from flaskapp.main.resources.schemas.review import ReviewSchema


class ReviewsAPI(Resource):
    """GET All Reviews"""

    def get(self, restroom_id):
        try:
            q = Review.query\
                .filter_by(restroom_id=restroom_id)\
                .filter(Review.description!=None)

            reviews = q.all()

            if reviews:
                return ReviewSchema(many=True).dump(reviews).data
            else:
                abort(app.config['NOT_FOUND'], message=app.config['REVIEW_NOT_FOUND'])
        except(DataError, NoResultFound):
            abort(app.config['NOT_FOUND'], message=app.config['REVIEW_NOT_FOUND'])


class ReviewAPI(Resource):
    """GET a specific Review"""

    def get(self, id):
        try:
            review = Review.query.get(id)
            if review:
                return ReviewSchema().dump(review).data
            else:
                abort(app.config['NOT_FOUND'], message=app.config['REVIEW_NOT_FOUND'])
        except(DataError, NoResultFound):
            abort(app.config['NOT_FOUND'], message=app.config['REVIEW_NOT_FOUND'])


class RestroomReviewAPI(Resource):
    """Post a review or create a new restroom and review"""

    def post(self):
        # check if a restroom exists using the lat and lng and if it doesn't then create the restroom if it does
        # then post a review to the corresponding restroom
        lat = request.json.pop('lat')
        lng = request.json.pop('lng')
        address = request.json.pop('address')

        name = request.json.pop('name')

        try:
            rr = Restroom.query.filter(and_(Restroom.lat==lat, Restroom.lng==lng)).one()

            request.json['restroomId'] = rr.id
            review, errors = ReviewSchema().load(request.json)

            if errors:
                abort(app.config['UNPROCESSABLE_ENTITY'], message=jsonify(errors))

            db.session.add(review)
            db.session.commit()

            review_dump, errors = ReviewSchema().dump(review)

            if errors:
                abort(app.config['UNPROCESSABLE_ENTITY'], message=jsonify(errors))

            return review_dump
        except NoResultFound:
            rr, errors = RestroomSchema().load({'address': address, 'name': name, 'lat': lat, 'lng': lng})

            if errors:
                abort(app.config['UNPROCESSABLE_ENTITY'], message=jsonify(errors))

            db.session.add(rr)
            db.session.commit()

            request.json['restroomId'] = rr.id
            review, errors = ReviewSchema().load(request.json)

            if errors:
                abort(app.config['UNPROCESSABLE_ENTITY'], message=jsonify(errors))

            db.session.add(review)
            db.session.commit()

            rr_dump, errors = RestroomSchema().dump(rr)

            if errors:
                abort(app.config['UNPROCESSABLE_ENTITY'], message=jsonify(errors))

            return rr_dump





