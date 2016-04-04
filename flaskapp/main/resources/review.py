
from flask import request, jsonify
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import DataError
from flaskapp.main.resources.models import Review
from flaskapp import app, db
from flaskapp.main.resources.schemas.review import ReviewSchema


class ReviewsAPI(Resource):
    """GET All Reviews or POST a review"""

    def get(self, restroom_id):
        try:
            q = Review.query.filter_by(restroom_id=restroom_id)

            reviews = q.all()

            if reviews:
                return ReviewSchema(many=True).dump(reviews).data
            else:
                abort(app.config['NOT_FOUND'], message=app.config['REVIEW_NOT_FOUND'])
        except(DataError, NoResultFound):
            abort(app.config['NOT_FOUND'], message=app.config['REVIEW_NOT_FOUND'])

    def post(self, restroom_id):
        discussion, errors = ReviewSchema().load(request.json)

        if errors:
            abort(app.config['UNPROCESSABLE_ENTITY'], message=jsonify(errors))

        db.session.add(discussion)
        db.session.commit()

        review_dump, errors = ReviewSchema().dump(discussion)

        if errors:
            abort(app.config['UNPROCESSABLE_ENTITY'], message=jsonify(errors))

        return review_dump


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
