from peewee import SqliteDatabase, Model, CharField, TextField, ForeignKeyField
from logs.logging_config import app_logger
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "database.db")
db = SqliteDatabase(db_path)


class Author(Model):
    name = CharField(unique=True)
    born = CharField(null=True)
    description = CharField(null=True)

    class Meta:
        database = db
        table_name = "authors"


class Tag(Model):
    name = CharField(unique=True)

    class Meta:
        database = db
        table_name = "tags"


class Quote(Model):
    content = TextField()
    author = ForeignKeyField(Author, backref="quotes")

    class Meta:
        database = db
        table_name = "quotes"


class QuoteTag(Model):
    quote = ForeignKeyField(Quote, backref="quote_tag")
    tag = ForeignKeyField(Tag, backref="quote_tags")

    class Meta:
        database = db
        table_name = "quote_tags"
        indexes = (
            (("quote", "tag"), True)
        )


try:
    db.connect()
    app_logger.info("Связь с базой данных установлена.")
    db.create_tables([Author, Tag, Quote, QuoteTag])

except Exception as exc:
    app_logger.warning(f"Ошибка при подключении к базе данных: {exc}")