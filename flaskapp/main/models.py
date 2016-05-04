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
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    review = db.relationship('Review')
    images_url = db.Column(db.String)

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

    @property
    def review_count(self):
        count = 0

        count_in_db = db.session.query(
            func.count(Review.id)
        ).filter_by(
            restroom_id=self.id
        ).one()[0]

        if count_in_db:
            count = count_in_db

        return count


class Review(db.Model):
    """
    Model for reviews
    """

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float)
    description = db.Column(db.String)
    date = db.Column(db.DateTime, server_default=func.now())
    title = db.Column(db.String)
    user = db.Column(db.String)

    restroom_id = db.Column(db.Integer, db.ForeignKey('restrooms.id'))
