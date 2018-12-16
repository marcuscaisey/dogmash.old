import pytest
import peewee

from dogmash import models, operations


@pytest.fixture(scope="module")
def db():
    """Empty test database to be used in all tests."""
    db = peewee.SqliteDatabase(":memory:")
    models.Dog.bind(db)
    models.Dog.create_table()
    return db


@pytest.fixture(autouse=True)
def txn(db):
    """Transaction fixture which automatically rolls back all changes after
    each test has finished, regardless of the result."""
    with db.atomic() as txn:
        yield
        txn.rollback()


def test_add_dog():
    file_name = "dogfilename.jpg"
    rating = 1000
    operations.add_dog(file_name)

    dogs = models.Dog.select()
    assert len(dogs) == 1
    dog = dogs[0]
    assert dog.file_name == file_name and dog.rating == rating


def test_create_dog_table(db):
    models.Dog.drop_table()
    operations.create_dog_table()
    assert models.Dog.table_exists()
