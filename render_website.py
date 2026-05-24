import json
import shutil
from pathlib import Path

from decouple import config
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

JSON_PATH = config('JSON_PATH', default='meta_data.json')


def on_reload():
    with open(JSON_PATH, 'r', encoding='utf-8') as file:
        books = json.load(file)

    pages = list(chunked(books, 20))
    count_pages = len(pages)

    pages_dir = Path('pages')
    if pages_dir.exists() and pages_dir.is_dir():
        shutil.rmtree(pages_dir)

    for num, books_page in enumerate(pages, 1):
        env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml'])
        )

        template = env.get_template('template.html')

        rendered_page = template.render(
            books=books_page,
            count_pages=count_pages,
            cur_page=num
        )

        page_path = Path(f'pages/index{num}.html')
        page_path.parent.mkdir(parents=True, exist_ok=True)
        with page_path.open(mode='w', encoding='utf8') as file:
            file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename='./pages/index1.html')


if __name__ == '__main__':
    main()
