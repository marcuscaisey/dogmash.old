import random
import string

import peewee
import pytest

from dogmash import config, models


@pytest.fixture(scope="session")
def db():
    """Empty test database to be used in all tests."""
    db = peewee.SqliteDatabase(":memory:")
    models.Dog.bind(db)
    models.Dog.create_table()
    return db


@pytest.fixture()
def txn(db):
    """Transaction fixture which automatically rolls back all changes after
    each test has finished, regardless of the result."""
    with db.atomic() as txn:
        yield
        txn.rollback()


@pytest.fixture
def create_dog(create_random_file_name):
    """Factory which creates and returns a Dog model. If file name or rating
    not given, then a random one is used."""

    def dog_factory(rating=None, file_name=None):
        file_name = (
            create_random_file_name() if file_name is None else file_name
        )
        rating = random.randint(0, 5000) if rating is None else rating
        return models.Dog.create(file_name=file_name, rating=rating)

    return dog_factory


@pytest.fixture
def create_random_file_name():
    """Factory which returns a random image file name."""

    def random_file_name_factory():
        length = random.randint(10, 15)
        chars = string.ascii_letters + string.digits + "-_"
        return f"{''.join(random.choice(chars) for _ in range(length))}.jpg"

    return random_file_name_factory
