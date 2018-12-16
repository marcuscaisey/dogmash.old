from . import models


def add_dog(file_name):
    """Add dog with image file name `file_name` to the dog table in the
    database. All dogs are added with a starting rating of 1000.

    Args:
        file_name (str): File name of image of dog.
    """
    models.Dog.create(file_name=file_name, rating=1000)


def create_dog_table():
    """Create dog table in the database."""
    models.Dog.create_table()
