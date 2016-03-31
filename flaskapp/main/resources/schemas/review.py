from marshmallow import fields, Schema
from flaskapp import ma


class ReviewSchema(Schema):
    """
    Marshmallow Schema class for the Review model.
    """

    id = fields.Integer()
    address = fields.String()
    rating = fields.Integer()
    description = fields.String()
    date = fields.DateTime()
    rr_name = fields.String()
    images = fields.String()

    uri = ma.URLFor('.reviewapi', id='<id>')
