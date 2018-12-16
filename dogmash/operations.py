from . import models


def create_dog_table():
    """Create dog table in the database."""
    models.Dog.create_table()
