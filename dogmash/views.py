import random

import flask

import dogmash
from dogmash import config, operations


@dogmash.app.route("/")
def index():
    dog1, dog2 = random.sample(operations.dogs(), 2)
    return flask.render_template("index.html", dog1=dog1, dog2=dog2)


@dogmash.app.route("/images/<path:filename>")
def dog_image(filename):
    return flask.send_from_directory(
        config.DOG_IMAGES_DIR, filename, as_attachment=True
    )
