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


def test_create_dog_table(db):
    models.Dog.drop_table()
    operations.create_dog_table()
    assert models.Dog.table_exists()
