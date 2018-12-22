import pytest

from dogmash import config, exceptions, models, operations


@pytest.mark.parametrize("dog_exists", [True, False])
def test_add_dog(txn, monkeypatch, create_dog, dog_exists):
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


def test_dogs(txn, create_dog):
    dogs = [create_dog() for _ in range(50)]
    assert operations.dogs() == dogs


@pytest.mark.parametrize("dog_in_table", [True, False])
def test_fill_database(
    txn,
    monkeypatch,
    tmp_path,
    create_random_file_name,
    create_dog,
    dog_in_table,
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


@pytest.mark.parametrize("dog_exists", [True, False])
def test_get_dog(txn, create_dog, dog_exists):
    if dog_exists:
        dog = create_dog()
        assert operations.get_dog(dog.id) == dog

    else:
        with pytest.raises(exceptions.DogDoesNotExist):
            print(operations.get_dog(1))
