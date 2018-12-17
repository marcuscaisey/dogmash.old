import pathlib

import peewee

current_dir = pathlib.Path(__file__).parent
PRAGMAS = {"journal_mode": "wal"}
db = peewee.SqliteDatabase(current_dir / "db.sqlite", pragmas=PRAGMAS)


class Dog(peewee.Model):
    """Dog model which holds a dog's rating and image file name."""

    file_name = peewee.TextField(unique=True)
    rating = peewee.IntegerField()

    class Meta:
        database = db
