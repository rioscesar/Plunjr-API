from flask_restful import Resource


class HelloWorld(Resource):
    """Test Call"""

    def get(self):
        return 'Hello World'

