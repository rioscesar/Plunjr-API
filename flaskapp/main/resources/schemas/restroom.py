from marshmallow import fields, Schema
from flaskapp import ma
from flaskapp.main.resources.schemas.review import ReviewSchema


class RestroomSchema(Schema):
    """
    Marshmallow Schema class for the Restroom model.
    """

    id = fields.Integer()
    name = fields.String()
    address = fields.String()
    averageRating = fields.Integer(attribute='average_rating')

    # this is actually a nested class
    reviews = fields.List(fields.Nested(ReviewSchema))

    uri = ma.URLFor('.restroomapi', id='<id>')
