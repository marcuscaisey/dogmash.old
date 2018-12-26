import random

import flask

import dogmash
from dogmash import calculations, config, models, operations


@dogmash.app.route("/")
def index():
    dog1, dog2 = random.sample(operations.dogs(), 2)
    return flask.render_template("index.html", dog1=dog1, dog2=dog2)


@dogmash.app.route("/images/<path:filename>")
def dog_image(filename):
    return flask.send_from_directory(
        config.DOG_IMAGES_DIR, filename, as_attachment=True
    )


@dogmash.app.route("/updateratings", methods=["POST"])
def update_ratings():
    """Calulcate/update the ratings/ranks of the winning/losing dogs and return
    their new ranks/ratings, associated rank/rating changes, and the details
    of the new dogs to be loaded.

    Request:
        POST /updateratings
        winner_id: ID of winning dog.
        loser_id: ID of losing dog.

    Response:
        {
            "winner": {
                "rank": New rank of winning dog,
                "rank_change": Change to winning dog's rank,
                "rating": New rating of winning dog,
                "rating_change": Change to winning dog's rating,
            },
            "loser": {
                "rank": New rank of losing dog,
                "rank_change": Change to losing dog's rank,
                "rating": New rating of losing dog,
                "rating_change": Change to losing dog's rating,
            },
            "dog1": {
                "id": ID of first new dog,
                "rating": Rating of first new dog,
                "rank": Rank of first new dog,
                "file_name": File name of first new dog,
            },
            "dog2": {
                "id": ID of second new dog,
                "rating": Rating of second new dog,
                "rank": Rank of second new dog,
                "file_name": File name of second new dog,
            }
        }
    """
    # Wrap operations in a transaction, so that the ratings are up to date
    # before they are modified.
    with models.db.atomic():
        winner = operations.get_dog(int(flask.request.form["winner_id"]))
        loser = operations.get_dog(int(flask.request.form["loser_id"]))

        old_winner_rank = winner.rank
        old_loser_rank = loser.rank
        old_winner_rating = winner.rating
        old_loser_rating = loser.rating

        winner.rating, loser.rating = calculations.new_elos(
            winner.rating, loser.rating, config.ELO_K
        )
        winner.save()
        loser.save()

    dog1, dog2 = random.sample(operations.dogs(), 2)
    data = {
        "winner": {
            "rank": winner.rank,
            "rank_change": format(old_winner_rank - winner.rank, "+"),
            "rating": winner.rating,
            "rating_change": format(winner.rating - old_winner_rating, "+"),
        },
        "loser": {
            "rank": loser.rank,
            "rank_change": format(old_loser_rank - loser.rank, "+"),
            "rating": loser.rating,
            "rating_change": format(loser.rating - old_loser_rating, "+"),
        },
        "dog1": {
            "id": dog1.id,
            "rating": dog1.rating,
            "rank": dog1.rank,
            "file_name": dog1.file_name,
        },
        "dog2": {
            "id": dog2.id,
            "rating": dog2.rating,
            "rank": dog2.rank,
            "file_name": dog2.file_name,
        },
    }

    return flask.jsonify(data), 200
