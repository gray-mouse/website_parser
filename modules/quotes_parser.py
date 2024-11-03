from bs4 import BeautifulSoup
import requests
from logs.logging_config import app_logger

class QuoteParser:
    def __init__(self, base_url):
        self.base_url = base_url

    def parse_quotes(self, html_content):
        try:
            app_logger.info(f"Начало сбора данных со страницы {self.base_url}")
            soup = BeautifulSoup(html_content, 'html.parser')
            quotes = soup.find_all("div", class_="quote")
            next_button = soup.find("li", class_="next")

            for quote in quotes:
                text = quote.find("span", class_="text").get_text(strip=True)
                author = quote.find("small", class_="author").get_text(strip=True)
                author_link = self.base_url + quote.find("a", href=True)["href"]
                tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]
                yield {
                    "text": text,
                    "author": author,
                    "author_link": author_link,
                    "tags": tags,
                    "next_url": self.base_url + next_button.find("a")["href"] if next_button else None
                }

        except Exception as exc:
            app_logger.error(f"Произошла ошибка во время парсинга страницы цитат. {exc}")


class AuthorFetcher:
    def fetch_author_info(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            app_logger.info(f"Начало сбора данных со страницы автора: {url}")
            soup = BeautifulSoup(response.text, 'html.parser')
            name = soup.find("h3", class_="author-title").get_text(strip=True)
            born_date = soup.find("span", class_="author-born-date").get_text(strip=True)
            born_location = soup.find("span", class_="author-born-location").get_text(strip=True)
            description = soup.find("div", class_="author-description").get_text(strip=True)
            app_logger.info(f"Данные автора успешно собраны.")
            return {
                "name": name,
                "born_date": born_date,
                "born_location": born_location,
                "description": description
            }
        else:
            app_logger.warning(f"Страница автора {url} не доступна. Код ответа {response.status_code}")
            return {
                "name": None,
                "born_date": None,
                "born_location": None,
                "description": None
            }
