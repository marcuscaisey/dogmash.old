import peewee

from . import config, exceptions, models


def add_dog(file_name):
    """Add dog with image file name `file_name` to the dog table in the
    database. All dogs are added with a starting rating of 1000.

    Args:
        file_name (str): File name of image of dog.

    Raises:
        exceptions.DogAlreadyExists: If a dog with `file_name` already exists
            in the dog table.
    """
    try:
        models.Dog.create(
            file_name=file_name, rating=config.DOG_INITIAL_RATING
        )
    except peewee.IntegrityError:
        raise exceptions.DogAlreadyExists


def create_dog_table():
    """Create dog table in the database."""
    models.Dog.create_table()


def dogs():
    """Return list of all dogs in the dog table.

    Returns:
        list of models.Dog: List of all dogs.
    """
    return list(models.Dog.select())


def fill_dog_table():
    """Search through the dog images directory and add any images which aren't
    already in it to the dog table."""
    for image_path in config.DOG_IMAGES_DIR.iterdir():
        try:
            add_dog(image_path.name)
        except exceptions.DogAlreadyExists:
            pass
