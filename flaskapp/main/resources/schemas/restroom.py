from marshmallow import fields, Schema, post_load

from flaskapp import ma
from flaskapp.main.models import Restroom
from flaskapp.main.resources.schemas.review import ReviewSchema
from flaskapp.main.resources.schemas.schema_utils import copy_dict_values_to_object_attrs


class RestroomSchema(Schema):
    """
    Marshmallow Schema class for the Restroom model.
    """

    id = fields.Integer()
    name = fields.String(allow_none=True)
    address = fields.String()
    averageRating = fields.Float(attribute='average_rating')
    reviewCount = fields.Integer(attribute='review_count')

    # this is actually a nested class
    review = fields.List(fields.Nested(ReviewSchema))

    uri = ma.URLFor('.restroomapi', id='<id>')

    @post_load
    def use_restroom_object(self, item):
        if item is None:
            return item

        if 'id' in item.keys():
            restroom = Restroom.query.get(item['id'])
        else:
            restroom = Restroom()

        copy_keys = ['name', 'address']

        copy_dict_values_to_object_attrs(copy_keys, item, restroom)

        return restroom
