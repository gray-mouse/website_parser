from .page_loader import PageLoader
from .quotes_parser import QuoteParser, AuthorFetcher
from databases.operations import add_author, add_quote, add_tag, link_quote_tag
from logs.logging_config import app_logger


class QuoteScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.current_url = base_url
        self.page_loader = PageLoader()
        self.quote_parser = QuoteParser(base_url)
        self.author_fetcher = AuthorFetcher()

    def scrape_quotes(self):
        while self.current_url:
            html_content, _ = self.page_loader.load_page(self.current_url)
            try:
                app_logger.info(f"Начало записи в базу данных со страницы {self.current_url}")
                for data in self.quote_parser.parse_quotes(html_content):
                    author_info = self.author_fetcher.fetch_author_info(data["author_link"])

                    author, created = add_author(
                        name=author_info['name'],
                        born=author_info['born_date'] + ' ' + author_info['born_location'] if
                        author_info['born_date'] and author_info['born_location'] else None,
                        description=author_info['description']
                    )

                    quote = add_quote(content=data['text'], author=author)

                    for tag_name in data['tags']:
                        tag = add_tag(name=tag_name)
                        link_quote_tag(quote=quote, tag=tag)

                app_logger.info("Запись прошла успешно!")

                self.current_url = data.get("next_url")
                app_logger.info(f"Переход на следующую страницу: {self.current_url}")

            except Exception as exc:
                app_logger.error(f"Ошибка записи в базу данных! {exc}")