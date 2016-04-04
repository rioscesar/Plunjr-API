from marshmallow import fields, Schema
from flaskapp import ma


class ReviewSchema(Schema):
    """
    Marshmallow Schema class for the Review model.
    """

    id = fields.Integer()
    rating = fields.Float()
    description = fields.String()
    date = fields.DateTime()
    images = fields.String()
    title = fields.String()
    user = fields.String()

    uri = ma.URLFor('.reviewapi', id='<id>')
