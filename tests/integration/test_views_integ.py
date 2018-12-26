import random

import pytest

import dogmash
from dogmash import config


@pytest.fixture
def client():
    return dogmash.app.test_client()


def test_update_ratings(txn, monkeypatch, mocker, client, create_dog):
    monkeypatch.setattr(config, "ELO_K", 32)

    dog1 = create_dog(rating=995)
    dog2 = create_dog(rating=1005)
    dog3 = create_dog(rating=1000)
    dog4 = create_dog(rating=1500)

    mocker.patch.object(random, "sample", return_value=[dog3, dog4])

    request_data = {"winner_id": dog1.id, "loser_id": dog2.id}
    response = client.post("/updateratings", data=request_data)

    assert response.json == {
        "winner": {
            "rank": 2,
            "rank_change": "+2",
            "rating": 1011,
            "rating_change": "+16",
        },
        "loser": {
            "rank": 4,
            "rank_change": "-2",
            "rating": 989,
            "rating_change": "-16",
        },
        "dog1": {
            "id": dog3.id,
            "rating": 1000,
            "rank": 3,
            "file_name": dog3.file_name,
        },
        "dog2": {
            "id": dog4.id,
            "rating": 1500,
            "rank": 1,
            "file_name": dog4.file_name,
        },
    }
