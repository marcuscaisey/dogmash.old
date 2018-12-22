class DogAlreadyExists(Exception):
    """Dog with this file name already exists in the dog table."""


class DogDoesNotExist(Exception):
    """Dog with this id doesn't exist in the dog table."""
