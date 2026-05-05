import json
from more_itertools import chunked
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def on_reload():
    with open('meta_data.json', 'r', encoding='utf-8') as file:
        books = json.load(file)

    pages = list(chunked(books, 20))

    for num, books_page in enumerate(pages, 1):
        env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml'])
        )

        template = env.get_template('template.html')

        rendered_page = template.render(
            books=books_page,
        )

        page_path = Path(f"pages/index{num}.html")
        page_path.parent.mkdir(parents=True, exist_ok=True)
        with page_path.open(mode='w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='./pages', default_filename='index1.html')
