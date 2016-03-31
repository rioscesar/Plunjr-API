from flask import Flask, Blueprint
from flask_restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config.from_envvar('CONFIG_PATH')

db = SQLAlchemy(app)
ma = Marshmallow(app)

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

# routes go here
from flaskapp.main.resources.review import ReviewsAPI, ReviewAPI
api.add_resource(ReviewsAPI, '/reviews', '/reviews/')
api.add_resource(ReviewAPI, '/reviews/<id>', 'reviews/<id>/')

app.register_blueprint(api_bp)
