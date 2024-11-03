from peewee import IntegrityError
from .models import Author, Tag, Quote, QuoteTag
from logs.logging_config import app_logger


def add_author(name, born=None, description=None):
    """Добавляет автора в базу данных, если он еще не существует."""
    try:
        author, created = Author.get_or_create(
            name=name,
            defaults={'born': born, 'description': description}
        )
        return author, created
    except IntegrityError as exc:
        app_logger.warning(f"Данные автора не записаны, т.к. они уже существуют. {exc} ")
        return Author.get(name=name), False


def add_quote(content, author):
    """Добавляет цитату в базу данных."""
    return Quote.create(content=content, author=author)


def add_tag(name):
    """Добавляет тег в базу данных, если он еще не существует."""
    tag, created = Tag.get_or_create(name=name)
    return tag


def link_quote_tag(quote, tag):
    """Связывает цитату с тегом в базе данных."""
    QuoteTag.create(quote=quote, tag=tag)
