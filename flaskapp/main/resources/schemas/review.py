from marshmallow import fields, Schema, post_load

from flaskapp import ma
from flaskapp.main.models import Review
from flaskapp.main.resources.schemas.schema_utils import copy_dict_values_to_object_attrs


class ReviewSchema(Schema):
    """
    Marshmallow Schema class for the Review model.
    """

    id = fields.Integer()
    rating = fields.Float()
    description = fields.String()
    date = fields.DateTime()
    title = fields.String()
    user = fields.String(allow_none=True)

    restroomId = fields.Integer(attribute='restroom_id')

    uri = ma.URLFor('.reviewapi', id='<id>')

    @post_load
    def use_review_object(self, item):
        if item is None:
            return item

        if 'id' in item.keys():
            review = Review.query.get(item['id'])
        else:
            review = Review()

        copy_keys = ['rating', 'description', 'images', 'title', 'user', 'restroom_id']

        copy_dict_values_to_object_attrs(copy_keys, item, review)

        return review
