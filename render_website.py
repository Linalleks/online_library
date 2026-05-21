import json
import shutil
from pathlib import Path

import click
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def render_pages(books):
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


def on_reload_wrapper(books):
    def callback():
        render_pages(books)
    return callback


@click.command(help='JSON_PATH: Путь к json-файлу с данными по книгам онлайн-библиотеки')
@click.argument('json_path', envvar='JSON_PATH', default='meta_data.json', type=click.Path(exists=True))
def main(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        books = json.load(file)
    render_pages(books)

    on_reload = on_reload_wrapper(books)
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename='./pages/index1.html')


if __name__ == '__main__':
    load_dotenv()
    main()
