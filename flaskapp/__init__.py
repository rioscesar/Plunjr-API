from flask import Flask, Blueprint
from flask_restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config.from_pyfile('../config.py')

db = SQLAlchemy(app)
ma = Marshmallow(app)

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

# routes go here
from flaskapp.main.resources.restroom import RestroomsAPI, RestroomAPI
api.add_resource(RestroomsAPI, '/restrooms', '/restrooms/')
api.add_resource(RestroomAPI, '/restrooms/<id>', 'restrooms/<id>/')

from flaskapp.main.resources.review import ReviewsAPI, ReviewAPI
api.add_resource(ReviewsAPI, '/restrooms/<restroom_id>/reviews', '/restrooms/<restroom_id>/reviews/')
api.add_resource(ReviewAPI, '/reviews/<id>', 'reviews/<id>/')

from flaskapp.main.resources.review import RestroomReviewAPI
api.add_resource(RestroomReviewAPI, '/reviews', '/reviews/')

from flaskapp.main.resources.hello import HelloWorld
api.add_resource(HelloWorld, '/')

app.register_blueprint(api_bp)
