from sqlalchemy import func

from flaskapp import db


class Restroom(db.Model):
    """
    Model for restrooms
    """

    __tablename__ = 'restrooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    review = db.relationship('Review')

    @property
    def average_rating(self):
        avg_rating = 0

        avg_rating_in_db = db.session.query(
            func.avg(Review.rating)
        ).filter_by(
            restroom_id=self.id
        ).one()[0]

        if avg_rating_in_db:
            avg_rating = avg_rating_in_db

        return avg_rating


class Review(db.Model):
    """
    Model for reviews
    """

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    description = db.Column(db.String)
    date = db.Column(db.DateTime)
    images = db.Column(db.String)

    restroom_id = db.Column(db.Integer, db.ForeignKey('restrooms.id'))
