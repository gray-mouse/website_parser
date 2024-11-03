from modules.scraper import QuoteScraper
from logs.logging_config import app_logger
from json_export import export_authors_data, export_authors_quotes_and_tags


if __name__ == "__main__":
    try:
        app_logger.info("Запуск программы...")
        base_url = 'http://quotes.toscrape.com'
        scraper = QuoteScraper(base_url)
        scraper.scrape_quotes()
        app_logger.info("Работа программы завершена.")
        export_authors_quotes_and_tags('authors_quotes_and_tags.json')
        export_authors_data('authors_data.json')
        app_logger.info("Файлы с цитатами и данными авторов сформированы")


    except Exception as exc:
        app_logger.error(f"Ошибка во время запуска программы: {exc}")
