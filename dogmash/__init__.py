import flask

from dogmash import operations

operations.fill_dog_table()

app = flask.Flask(__name__)

import dogmash.views
