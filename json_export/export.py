import json
from databases.models import Author

def export_authors_quotes_and_tags(file_path):
    data = []

    for author in Author.select():
        author_data = {
            'name': author.name,
            'quotes': []
        }

        for quote in author.quotes:
            quote_data = {
                'content': quote.content,
                'tags': [tag.tag.name for tag in quote.quote_tag]
            }
            author_data['quotes'].append(quote_data)

        data.append(author_data)

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def export_authors_data(file_path):
    data = []

    for author in Author.select():
        author_data = {
            'name': author.name,
            'born': author.born,
            'description': author.description
        }

        data.append(author_data)

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


# if __name__ == "__main__":
#     export_authors_quotes_and_tags('authors_quotes_and_tags.json')
#     export_authors_data('authors_data.json')