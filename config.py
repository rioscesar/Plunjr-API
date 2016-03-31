### BASE URL ###
BASE_URL = '/api'

### HTML STATUS CODES ###
OK = 200
UNPROCESSABLE_ENTITY = 422
NOT_FOUND = 404

# SQLAlchemy config (only example not actually set)
SQLALCHEMY_DATABASE_URI = "postgresql://plunjr:plunjr@localhost/plunjr"

### USER-FACING FLASH ERROR STRINGS ###
REVIEW_NOT_FOUND = 'Could not retrieve review!'
RESTROOM_NOT_FOUND = 'Could not retrieve restroom!'
