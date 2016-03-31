from flaskapp import db


class Review(db.Model):
    """
    Model for reviews
    """

    id = db.Column(db.Integer)
    address = db.Column(db.String)
    rating = db.Column(db.Integer)
    description = db.Column(db.String)
    date = db.Column(db.DateTime)
    rr_name = db.Column(db.String)
    images = db.Column(db.String)
