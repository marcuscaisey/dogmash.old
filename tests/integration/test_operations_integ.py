import random
import string

import peewee
import pytest

from dogmash import config, exceptions, models, operations


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


@pytest.fixture
def create_dog(create_random_file_name):
    """Factory which returns a dog with a given file name and a rating of
    `config.DOG_INITIAL_RATING`. If no file name is given, then the dog is
    created with a random file name."""

    def dog_factory(file_name=None):
        file_name = (
            create_random_file_name() if file_name is None else file_name
        )
        rating = config.DOG_INITIAL_RATING
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


@pytest.mark.parametrize("dog_exists", [True, False])
def test_add_dog(monkeypatch, create_dog, dog_exists):
    monkeypatch.setattr(config, "DOG_INITIAL_RATING", 2000)

    if dog_exists:
        dog = create_dog()
        with pytest.raises(exceptions.DogAlreadyExists):
            operations.add_dog(dog.file_name)

    else:
        operations.add_dog("dogfilename.jpg")
        dogs = models.Dog.select()
        assert len(dogs) == 1
        dog = dogs[0]
        assert dog.file_name == "dogfilename.jpg" and dog.rating == 2000


def test_create_dog_table(db):
    models.Dog.drop_table()
    operations.create_dog_table()
    assert models.Dog.table_exists()


def test_dogs(create_dog):
    dogs = [create_dog() for _ in range(50)]
    assert operations.dogs() == dogs


@pytest.mark.parametrize("dog_in_table", [True, False])
def test_fill_database(
    monkeypatch, tmp_path, create_random_file_name, create_dog, dog_in_table
):
    monkeypatch.setattr(config, "DOG_IMAGES_DIR", tmp_path)

    file_names = [create_random_file_name() for _ in range(5)]
    for file_name in file_names:
        (tmp_path / file_name).touch()

    if dog_in_table:
        create_dog(file_names[0])

    operations.fill_dog_table()

    dogs = models.Dog.select()
    assert len(dogs) == 5
    dog_file_names = [dog.file_name for dog in dogs]
    assert all(file_name in dog_file_names for file_name in file_names)
