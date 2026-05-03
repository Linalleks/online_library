import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

        "title": "Роковой поцелуй",
        "author": "Патрацкая Наталья",
        "img_src": "img/nopic.gif",
        "book_path": "books/5648-Роковой поцелуй.txt",
        "comments": [],
        "genres": "Научная фантастика, Прочие Детективы, Прочие приключения."
def main():
    with open('meta_data.json', 'r', encoding='utf-8') as file:
        books = json.load(file)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        books=books,
        # wine_groups=wine_groups
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()